import React, { Component } from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";


export default class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      password: "",
      loggedIn: false, // Track login state
      errorMessage: "", // Track error message
    };
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleSubmit = async (event) => {
    event.preventDefault();

    const { email, password } = this.state;

    try {
      const response = await axios.post("http://localhost:5000/signin", {
        email,
        password,
      });

      if (response.status === 200) {
        console.log(email)
        window.localStorage.setItem("email", email)
        // Sign-in successful
        this.setState({ loggedIn: true });
      } else {
        // Sign-in failed
        this.setState({ errorMessage: response.data.message });
      }
    } catch (error) {
      console.error("Error signing in:", error);
      this.setState({ errorMessage: "Error signing in" });
    }
  };

  render() {
    const { email, password, loggedIn, errorMessage } = this.state;

    // Redirect to main page if logged in
    if (loggedIn) {
      return <Navigate to="/mainpage" />;
    }

    return (
      <form onSubmit={this.handleSubmit}>
        <h3>Sign In</h3>

        <div className="mb-3">
          <label>Email address</label>
          <input
            type="email"
            className="form-control"
            placeholder="Enter email"
            name="email"
            value={email}
            onChange={this.handleChange}
          />
        </div>

        <div className="mb-3">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            placeholder="Enter password"
            name="password"
            value={password}
            onChange={this.handleChange}
          />
        </div>

        <div className="d-grid">
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
        {errorMessage && <p className="text-danger">{errorMessage}</p>}
      </form>
    );
  }
}
