// App.js

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const StyledTextInput = ({
  placeholder,
  value,
  onChangeText,
  onFocus,
  onBlur,
  isFocused
}) => {
  return (
    <div className="inputContainer">
      <input
        className={isFocused ? 'input inputFocused' : 'input'}
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChangeText(e.target.value)}
        onFocus={onFocus}
        onBlur={onBlur}
      />
    </div>
  );
};

const App = () => {
  const [name, setName] = useState('');
  const [phoneto, setPhoneto] = useState('');
  const [problem, setProblem] = useState('');
  const [age, setAge] = useState('');
  const [location, setLocation] = useState('');
  const [gender, setGender] = useState('');
  const [message, setMessage] = useState('');
  const [textVisible, setTextVisible] = useState(true);
  const [isFocused, setIsFocused] = useState({
    name: false,
    phoneto: false,
    problem: false,
    age: false,
    location: false,
    gender: false,
  });

  const inputRefs = {
    name: React.createRef(),
    phoneto: React.createRef(),
    problem: React.createRef(),
    age: React.createRef(),
    location: React.createRef(),
    gender: React.createRef(),
  };

  const handleFocus = (field) => {
    setIsFocused((prev) => ({
      ...prev,
      [field]: true,
    }));
  };

  const handleBlur = (field) => {
    setIsFocused((prev) => ({
      ...prev,
      [field]: false,
    }));
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/post-data', {
        name,
        phoneto,
        problem,
        age,
        location,
        gender,
      });
      setMessage(response.data.message);
      setTextVisible(true);
    } catch (error) {
      console.error(error);
      setMessage('Error submitting data');
      setTextVisible(true);
    }
  };

  const handleTextPress = () => {
    setTextVisible(false);
  };

  return (
    <div className="app">
    <header className="header">
      <h1>Create Profile</h1>
    </header>
    <div className="container">
      <StyledTextInput
        placeholder="Name"
        value={name}
        onChangeText={setName}
        onFocus={() => handleFocus('name')}
        onBlur={() => handleBlur('name')}
        isFocused={isFocused.name}
      />
      <StyledTextInput
        placeholder="Phone To"
        value={phoneto}
        onChangeText={setPhoneto}
        onFocus={() => handleFocus('phoneto')}
        onBlur={() => handleBlur('phoneto')}
        isFocused={isFocused.phoneto}
      />
      <StyledTextInput
        placeholder="Problem"
        value={problem}
        onChangeText={setProblem}
        onFocus={() => handleFocus('problem')}
        onBlur={() => handleBlur('problem')}
        isFocused={isFocused.problem}
      />
      <StyledTextInput
        placeholder="Age"
        value={age}
        onChangeText={setAge}
        onFocus={() => handleFocus('age')}
        onBlur={() => handleBlur('age')}
        isFocused={isFocused.age}
      />
      <StyledTextInput
        placeholder="Location"
        value={location}
        onChangeText={setLocation}
        onFocus={() => handleFocus('location')}
        onBlur={() => handleBlur('location')}
        isFocused={isFocused.location}
      />
      <StyledTextInput
        placeholder="Gender"
        value={gender}
        onChangeText={setGender}
        onFocus={() => handleFocus('gender')}
        onBlur={() => handleBlur('gender')}
        isFocused={isFocused.gender}
      />
      <button className="submitBtn" onClick={handleSubmit}>
        Submit
      </button>
      {message && textVisible && (
        <div className="message" onClick={handleTextPress}>
          {message}
        </div>
      )}
      </div>
    </div>
    
  );
};

export default App;
