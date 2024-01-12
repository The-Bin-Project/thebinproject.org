import React, { useState, useEffect } from 'react';
import styles from './SelectFrames.module.css';

function SelectFrames() {
    const [images, setImages] = useState([]);

    useEffect(() => {
        // Fetch the list of images from your server
        fetch('http://127.0.0.1:5000/get-images')
            .then(response => response.json())
            .then(data => {
                setImages(data.images); // Assuming the response contains an array of image filenames
            })
            .catch(error => console.error('Error fetching images:', error));
    }, []);

    const handleImageClick = (imageName) => {
        if (window.confirm(`Do you want to delete this image: ${imageName}?`)) {
            fetch(`http://127.0.0.1:5000/delete-image/${imageName}`, { method: 'DELETE' })
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
             <h1 className={styles.heading}> Split Frames</h1>
            <p1 className={styles.paragraph}>The images below depict each plate detected by the camera. Please go through these frames and delete those which are redundant or incorrectly identified by clicking on the picture. </p1>
            <br></br>
            <br></br>
        <div className={styles.gridContainer}>
            {images.map((image, index) => (
    <img
            key={index}
                src={`http://127.0.0.1:5000/images/${image}`} // Update with the correct server URL
                 alt={`Processed frame ${index}`}
                className={styles.gridImage}
                onClick={() => handleImageClick(image)}
                onError={(e) => { e.target.onerror = null; e.target.style.display = 'none'; }} // Hide if cannot load
    />
))}
        </div>
        <button className={styles.button}>Done</button>
        </div>
    );
}

export default SelectFrames;
