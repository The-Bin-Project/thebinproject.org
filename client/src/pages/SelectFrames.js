import React, { useState, useEffect } from 'react';
import styles from './SelectFrames.module.css';
import {useLocation,useNavigate} from 'react-router-dom';
import swal from 'sweetalert';
import Swal from 'sweetalert2';

function SelectFrames() {
    const location = useLocation();
    const [images, setImages] = useState([]);
    const navigate = useNavigate(); 
    const [groupName, setGroupName] = useState('');
    const [schoolName, setSchoolName] = useState(location.state); 
    const [foldername, setFoldername] = useState('');
    const [goModelData, setGoModelData] = useState(null); // State to store data from goModel
    const goModel = () => {
        swal({
            title: "Loading...",
            text: "Please wait while we process your request.",
            icon: "info",
            buttons: false, // No buttons, as this is a loading message
            timer: 3000, // Optional: close alert automatically after 3000ms
        });
    
        fetch("http://127.0.0.1:5000" + '/classify_plates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ schoolName: schoolName, groupName: groupName }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.message === "ok") {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    buttonStyling: false,
                    text: 'Video processed successfully!',
                });
            }
            setGoModelData(data.results_flattened);
            swal.close(); // Close the loading alert
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                buttonStyling: false,
                text: 'An error occurred while processing your request.',
            });
        });
    };
    
    const goToDash = () => {
        navigate('/school',{state:{schoolName:schoolName}});
    };

    useEffect(() => {
        // Fetch the list of images from your server
        try{
            setSchoolName(location.state.schoolName);
            setGroupName(location.state.groupName);
        }
        catch(err){
            alert("Please login before entering this page")
            navigate('/');
        }
        fetch("http://127.0.0.1:5000" + '/get-all-images')
            .then(response => response.json())
            .then(data => {
                setImages(data.images); // Assuming the response contains an array of image filenames
                setFoldername(data.foldername)
            })
            .catch(error => console.error('Error fetching images:', error));
    }, []);

    const handleImageClick = (imageName) => {
        if (window.confirm(`Do you want to delete this image: ${imageName}?`)) {
            fetch("http://127.0.0.1:5000" + `/delete-image/${imageName}`, { method: 'DELETE' })
                .then(response => response.json())
                .then(data => {
                    if(data.message === "Image deleted") {
                        // Remove the image from the state as well, to update the UI
                        setImages(images.filter(image => image !== imageName));
                        // alert(`Image ${imageName} has been deleted.`);
                    }
                })
                .catch(error => console.error('Error deleting image:', error));
        }
    };
    


    return (
        <div>
             <h1 className={styles.heading}> Select Frames</h1>
            <p1 className={styles.paragraph}>The images below depict each plate detected by the camera. Please go through these frames and delete those which are redundant or incorrectly identified by clicking on the picture. </p1>
            <br></br>
            <br></br>
        <div className={styles.gridContainer}>
            {images.map((image, index) => (
    <img
            key={index}
                src={"http://127.0.0.1:5000" + `/images/${image}`} // Update with the correct server URL
                 alt={`Processed frame ${index}`}
                className={styles.gridImage}
                onClick={() => handleImageClick(image)}
                onError={(e) => { e.target.onerror = null; e.target.style.display = 'none'; }} // Hide if cannot load
    />
))}
        </div>
        <button onClick={goModel}className={styles.button}>Classify</button>
        <br></br>
        <br></br>
        <button onClick={goToDash}className={styles.button}>Go Back to Dashboard</button>
        <br></br>
        <br></br>
        </div>
    );
}

export default SelectFrames;
