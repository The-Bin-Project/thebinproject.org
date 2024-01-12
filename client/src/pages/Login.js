import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import styles from './Login.module.css';

function Login() {
  // State for username and password
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  // Hook for navigation
  const navigate = useNavigate();

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent the default form submit action
    // Check if credentials match
    if (username === "uwc_east" && password === "secret") {
      navigate('/admin'); // Navigate to /admin if credentials match
    } else {
      alert('Invalid credentials'); // Alert the user if credentials do not match
    }
  };

  return (
    <div id="login">
      <section>
        <h1 className={styles.heading2}>Login</h1>
        <div className={styles.card}>
          <p className={styles.infoText}>If you are a registered school please enter your username and password to proceed.</p>
          <form className={styles.Form} onSubmit={handleSubmit}>
            <br />
            <input 
              type="text" 
              placeholder="Username" 
              className={styles.inputBox} 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} // Update username state on change
            />
            <br />
            <input 
              type="password" 
              placeholder="Password" 
              className={styles.inputBox} 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} // Update password state on change
            />
            <br />
            <button type="submit">Login</button>
          </form>
        </div>
      </section>
    </div>
  );
}

export default Login;
