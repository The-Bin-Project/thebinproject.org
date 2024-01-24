import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate from react-router-dom
import styles from "./Login.module.css";

function Login() {
    // State for username and password
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    // Hook for navigation
    const navigate = useNavigate();

    // Function to handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent the default form submit actionn
        // Check if credentials match

        console.log ("SEINDING REUEST")
        const response = await fetch(
            process.env.REACT_APP_BACKEND + "/check-login",
            {
                method: "POST",
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
                headers: {
                    "Content-Type": "application/json", // Ensure you're sending the data as JSON
                },
            }
        );
        console.log ("RECEIVED RESPONSE")

        const data = await response.json();
        if (data.message == "ok") {
            alert("Login Successful");
            navigate("/school", { state: { schoolName: username } });
        } else if (data.message == "no") {
            alert("Invalid Credentials");
        }

        console.log(data);
        // if (username === "uwc_east" && password === "secret") {
        //   navigate('/admin'); // Navigate to /admin if credentials match
        // } else {
        //   alert('Invalid credentials'); // Alert the user if credentials do not match
        // }
    };

    return (
        <div id="login">
            <section>
                <h1 className={styles.heading2}>Login</h1>
                <div className={styles.card}>
                    <p className={styles.infoText}>
                        If you are a registered school please enter your
                        username and password to proceed.
                    </p>
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
