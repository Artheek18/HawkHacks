from flask import Flask, request, jsonify
from twilio.rest import Client
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/post-data', methods=['POST'])
def post_data():
    data = request.get_json()
    name = data.get('name')
    phoneto = data.get('phoneto')
    problem = data.get('problem')
    age = data.get('age')
    location = data.get('location')
    gender = data.get('gender')
    account_sid = os.environ.get('TWILIO_SID')
    auth_token = os.environ.get('TWILIO_AUTH')

    client = Client(account_sid, auth_token)

    # Create call
    call = client.calls.create(
        twiml=f'<Response><Say>Emergency! {name} has had an emergency. First responders have been noted at {location}</Say></Response>',
        to=phoneto,
        from_='+13656580913'
    )
    print(call.sid)

    # Create message
    message = client.messages.create(
        body=f'Warning! VitalSense, Emergency! {name} has had an emergency. First responders have been noted at {location}',
        from_='+13656580913',
        to=phoneto
    )
    print(message.sid)

    return jsonify(message="success"), 200

if __name__ == '__main__':
    app.run(debug=True)