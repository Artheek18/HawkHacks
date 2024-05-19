import React, { Component } from "react";
import axios from "axios";
import "./signup.css"; // Import CSS file for custom styles

export default class SignUp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      message: "",
      phoneNumber: "",
    };
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleSubmit = async (event) => {
    event.preventDefault();

    const {
      firstName,
      lastName,
      email,
      password,
      phoneNumber,
    } = this.state;

    try {
      const response = await axios.post("http://127.0.0.1:5000/signup", {
        firstName,
        lastName,
        email,
        password,
        phoneNumber,
      });

      this.setState({ message: response.data.message });
    } catch (error) {
      this.setState({ message: "Error submitting data" });
      console.error(error);
    }
  };

  render() {
    const {
      firstName,
      lastName,
      email,
      password,
      message,
      phoneNumber,
    } = this.state;

    return (
      <div className="signup-container">
        <form className="signup-card" onSubmit={this.handleSubmit}>
          <h3>Sign Up</h3>

          <div className="mb-3">
            <label>First name</label>
            <div className="input-container">
              <input
                type="text"
                className="form-control"
                placeholder="First name"
                name="firstName"
                value={firstName}
                onChange={this.handleChange}
              />
              <span className="icon">&#x1F464;</span> {/* Person icon */}
            </div>
          </div>

          <div className="mb-3">
            <label>Last name</label>
            <div className="input-container">
              <input
                type="text"
                className="form-control"
                placeholder="Last name"
                name="lastName"
                value={lastName}
                onChange={this.handleChange}
              />
              <span className="icon">&#x1F464;</span> {/* Person icon */}
            </div>
          </div>

          <div className="mb-3">
            <label>Email address</label>
            <div className="input-container">
              <input
                type="email"
                className="form-control"
                placeholder="Enter email"
                name="email"
                value={email}
                onChange={this.handleChange}
              />
              <span className="icon">&#x2709;</span> {/* Email icon */}
            </div>
          </div>

          <div className="mb-3">
            <label>Password</label>
            <div className="input-container">
              <input
                type="password"
                className="form-control"
                placeholder="Enter password"
                name="password"
                value={password}
                onChange={this.handleChange}
              />
              <span className="icon">&#x1F512;</span> {/* Lock icon */}
            </div>
          </div>

          <div className="mb-3">
            <label>Emergency Contact</label>
            <div className="input-container">
              <input
                type="text"
                className="form-control"
                placeholder="Enter number"
                name="phoneNumber"
                value={phoneNumber}
                onChange={this.handleChange}
              />
              <span className="icon">&#x260E;</span> {/* Phone icon */}
            </div>
          </div>

          <div className="d-grid">
            <button type="submit" className="btn btn-primary">
              Sign Up
            </button>
          </div>
          {message && <p className="forgot-password text-right">{message}</p>}
        </form>
      </div>
    );
  }
}
