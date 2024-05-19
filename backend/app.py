from flask import Flask, request, jsonify, flash
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import googlemaps
import csv
from twilio.rest import Client
import requests
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image



project_id = "decent-surf-422403-v7"


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Connect to MongoDB Atlas using environment variable
MONGO_URL = os.getenv('MONGO_URL')
# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Google Maps API credentials
#GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
#gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable not set")
else:
    client = MongoClient(MONGO_URL)
    db = client.get_database('DrivingDetection')  # Replace with your database name
    users_collection = db['users']
    print("Connected to MongoDB, database name:", db.name)


# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}  # Allow specific file types
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if the filename extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        data = request.get_json()
        print("Received data:", data)
        
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        password = data.get('password')

        # Validate required fields
        if not first_name or not last_name or not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if user already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"message": "User already exists"}), 400

        # Insert the new user
        new_user = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": hashed_password
        }
        users_collection.insert_one(new_user)
        print("User created successfully:", new_user)
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        print("Error inserting user:", e)
        return jsonify({"message": "Internal server error"}), 500

@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate required fields
        if not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        # Find the user by email
        
        user = users_collection.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Login successful", "id": email}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    except Exception as e:
        print("Error during signin:", e)
        return jsonify({"message": "Internal server error"}), 500

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
@app.route('/speed-limits', methods=['POST'])
def get_speed_limits():
    try:
      # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 400
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read the file to get speed and location data (assuming CSV with 'location' and 'speed' columns)
            #speed_limits = []
            difference = []
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    speed_limit = float(row['speedlimit'])
                    speed = float(row['speed'])
                    if speed_limit is not None:
                        difference.append((speed - speed_limit))
            # Assuming the user is authenticated and we have user_id or email in request headers or body
            user_email = request.headers.get('User-Email')
            if user_email:
                user = users_collection.find_one({"email": user_email})
                if user:
                    # Update the user's document with the trainedArray field
                    users_collection.update_one(
                        {"email": user_email},
                        {"$set": {"trainedArray": difference}}
                    )
                    return jsonify({"message": "Speed limits and differences stored successfully", "trainedArray": difference}), 200
                else:
                    return jsonify({"message": "User not found"}), 404
            else:
                return jsonify({"message": "User email not provided"}), 400
                
        else:
            return jsonify({"message": "File type not allowed"}), 400

    except Exception as e:
        print("Error checking speed limits:", e)
        return jsonify({"message": "Internal server error"}), 500
    
def _build_cors_preflight_response():
    response = jsonify({"message": "Preflight OK"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response


@app.route('/test-upload', methods=['POST'])
def analyze_driving():
    try:
      # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 400
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read the file to get speed and location data (assuming CSV with 'location' and 'speed' columns)
            #speed_limits = []
            test_difference = []
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    speed_limit = float(row['speedlimit'])
                    speed = float(row['speed'])
                    if speed_limit is not None:
                        test_difference.append((speed - speed_limit))

        user_email = request.headers.get('User-Email')
        if not user_email:
            return jsonify({"message": "User email not provided"}), 400

        user = users_collection.find_one({"email": user_email})
        if not user or 'trainedArray' not in user:
            return jsonify({"message": "No trained data found for user"}), 404
        

        trained_array = user['trainedArray']

        

        # vertexai.init(project=project_id, location="us-central1")
        # model = GenerativeModel(model_name="gemini-1.0-pro-002")

        # #Text prompt
        # response = model.generate_content(
        #     "Given {trained_array} which represents how the driver normally drives compared to the speed\
        #           limit, and {tested_array} which represents how they are driving currently. Both arrays\
        #              indicate the differences in speed versus the speed limit, where a negative value \
        #                 indicates driving below the speed limit and a positive value indicates driving\
        #              above the speed limit: Determine if the driver is exhibiting signs of drunk driving,\
        #                   just Yes or No do not give paragraph just give 1 word response of yes or no, \
        #                     Yes if the average is off or no if its close. "               
        # )
        # print(response.text)
        # return jsonify({"message": "Analysis successful"}), 200

        # Assuming the user is authenticated and we have user_id or email in request headers or body
       
        user_email = request.headers.get('User-Email')
        if user_email:
            user = users_collection.find_one({"email": user_email})
            if user:
                # Update the user's document with the trainedArray field
                users_collection.update_one(
                    {"email": user_email},
                    {"$set": {"testArray": test_difference}}
                )
                return jsonify({"message": "Speed limits and differences stored successfully"}), 200
            else:
                return jsonify({"message": "User not found"}), 404
        else:
            return jsonify({"message": "User email not provided"}), 400
            
        
        # if response.status_code == 200:
        #     hypothesis = response.json().get('hypothesis')
        #     return jsonify({"message": "Analysis successful", "hypothesis": hypothesis}), 200
        # else:
        #     return jsonify({"message": "Error analyzing data", "details": response.text}), 500
 
    except Exception as e:
        print("Error analyzing driving data:", e)
        return jsonify({"message": "Internal server error"}), 500

@app.route('/video-upload', methods=['POST'])
def upload_video():

        #VideoPrompt
        user_email = request.headers.get('User-Email')
        if not user_email:
           return jsonify({"message": "User email not provided"}), 400

        user = users_collection.find_one({"email": user_email})
        if not user or 'trainedArray' not in user:
            return jsonify({"message": "No trained data found for user"}), 404
        
        trained_array = user['trainedArray']
        tested_array = user['testArray']
        vertexai.init(project=project_id, location="us-central1")

        vision_model = GenerativeModel(model_name="gemini-1.0-pro-vision-001")

        # Generate text
        response = vision_model.generate_content(
            [
                Part.from_uri(
                    #gs://drunk_driver/Untitled video - Made with Clipchamp.mp4
                    #gs://drunk_driver/Boring Driving Video.mp4
                    "gs://drunk_driver/Untitled video - Made with Clipchamp.mp4", mime_type="video/mp4"
                ),
                "After analsying {trained_array} which is the (speed - speed limit) for how they normally drive\
                and {tested_array} is (speed - speed limit) is how they are currently driving and then looking at\
                the video of how they are driving, is the driver impaired? Just give 1 for likely impaired if \
                in video person is swirving and 0 for normal.\
                Just return one number either 1 or 0, no words or letters."
            ]
        )
        name = user['firstName']
        phoneto = TWILIO_PHONE_NUMBER
        print(response.text)
        if (response.text == " 1"):
            # Make a call
            call = client.calls.create(
                twiml=f'<Response><Say>Emergency! {name} is driving impaired. First responders have been noted </Say></Response>',
                to=phoneto,
                from_="+13656580913"
            )

            # Send a message
            message = client.messages.create(
                body=f'Warning! VitalSense, Emergency! {name} is driving impaired. First responders have been noted',
                from_="+13656580913",
                to=phoneto
            )
        else:
            print("Not Impaired")
        return jsonify({"message": "hi"}), 200 

if __name__ == '__main__':
    app.run(debug=True)
