import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./AdminInterface.module.css";

function AdminInterface() {
	const [selectionDimensions, setSelectionDimensions] = useState([]); // [x1, y1, x2, y2]
	const [selectionDimensions2, setSelectionDimensions2] = useState([]); // [x1, y1, x2, y2
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const navigate = useNavigate();


    const sendData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/split-frames', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Ensure you're sending the data as JSON
                },
                body: JSON.stringify({
                    selectionDimensions: selectionDimensions,
                    selectionDimensions2: selectionDimensions2,
                }), // Convert the data to JSON
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Handle the response here, if needed
            const data = await response.json();
            console.log(data);
            if(data.message=="ok"){
                alert("Data processed successfully")
                navigate('/selectframes');
                
            }

        } catch (error) {
            console.error('Error during the file upload:', error);
        }
    };


    
    // const handleVideoUpload = files => {
    //     const uploaded = [...uploadedFiles];
    //     let limitExceeded = false;
    //     files.some((file) => {
    //       if (uploaded.findIndex(f => f.name === file.name) === -1) {
    //         uploaded.push(file);
    //         if (uploaded.length === numberOfVids) setFileLimit(true);
    //         if (uploaded.length > numberOfVids) {
    //           alert(`You can only add a maximum of ${numberOfVids} files`);
    //           setFileLimit(false);
    //           limitExceeded = true;
    //           return true;
    //         }
    //       }
    //     });
      
    //     if (!limitExceeded) setUploadedFiles(uploaded)
    //   };
      
      const handleFileUpload = (event) => {
        setUploadedFiles(prevFiles => [...prevFiles, ...Array.from(event.target.files)]);
    };

    const uploadAllFiles = async () => {
        try {
            // Create an array of promises from the uploadData function
            const uploadPromises = uploadedFiles.map(file => uploadData(file));
            // Wait for all files to be uploaded
            await Promise.all(uploadPromises);
            // If all files are uploaded successfully, display an alert
            alert("All videos uploaded successfully! We are now processing your data, this may take a few minutes.");
        } catch (error) {
            console.error('Error during the file uploads:', error);
            alert("An error occurred during the uploads.");
        }
    };
    
    const uploadData = async (file) => {
        const formData = new FormData();
        formData.append('video', file);
        
        const response = await fetch('http://127.0.0.1:5000/video-upload', {
            method: 'POST',
            body: formData,
        });
    
        if (!response.ok) {
            // If the response is not ok, throw an error to be caught by the try...catch
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Return the response JSON to be processed or logged
    };
    
    
	// console.log("url", videoFile)

    return (
        <div>
            <h1 className={styles.heading}> Classification Interface</h1>
            <p1 className={styles.paragraph}>Welcome! Thank you for being a part of Project Bin in an effort to reduce waste through classification. Please upload the video files of the bin in the week/group you would like to analyze. </p1>
            <br></br>
            <br></br>
            <input
                type="file"
                accept="video/*"
                multiple
                onChange={handleFileUpload}
                className={styles.uploadInput}
            />
         <br></br>
            <br></br>
            <button className={styles.button}onClick={uploadAllFiles}>Done</button>
            <p className={styles.bold}>Files Uploaded:</p>
            {uploadedFiles.map((file, index) => (
               <div> <div className={styles.list} key={index}>{file.name}</div><br></br></div>
            ))}
       
        </div>
    );
}
export default AdminInterface;