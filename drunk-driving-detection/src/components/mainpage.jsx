import React, { useState } from "react";
import axios from "axios";
import "./mainpage.css";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [downloadLink, setDownloadLink] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log(window.localStorage.getItem("email"));
      await axios.post(
        "http://localhost:5000/speed-limits",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "User-Email": window.localStorage.getItem("email"),
          },
        }
      );
      setError("");
    } catch (error) {
      console.error("Error uploading file", error);
      setError("Error uploading file");
    }
  };

  const uploadTest = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log(window.localStorage.getItem("email"));
      await axios.post(
        "http://localhost:5000/test-upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "User-Email": window.localStorage.getItem("email"),
          },
        }
      );
      setError("");
    } catch (error) {
      console.error("Error uploading file", error);
      setError("Error uploading file");
    }
  };

  const uploadVid = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log(window.localStorage.getItem("email"));
      await axios.post(
        "http://localhost:5000/video-upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "User-Email": window.localStorage.getItem("email"),
          },
        }
      );
      setError("");
    } catch (error) {
      console.error("Error uploading file", error);
      setError("Error uploading file");
    }
  };

  return (
    <div className="main-container">
      <div className="file-upload">
        <form onSubmit={handleSubmit} className="file-form">
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Upload Train</button>
        </form>
        <form onSubmit={uploadTest} className="file-form">
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Upload Test</button>
        </form>
        <form onSubmit={uploadVid} className="submit-form">
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Submit</button>
        </form>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div>
          <h2>Results:</h2>
          {downloadLink && (
            <a href={downloadLink} download="results.txt">
              Download Results
            </a>
          )}
          </div>
      </div>
    </div>
  );
}

export default FileUpload;
