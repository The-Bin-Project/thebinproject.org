import React, { useState, useEffect, useRef } from "react";
import { useNavigate,useLocation } from "react-router-dom";
import styles from "./AdminInterface.module.css";
import Swal from "sweetalert2";

function AdminInterface() {
    const [videos, setVideos] = useState([]);
    const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
    const [selections, setSelections] = useState({});
    const [selectionDimensions1, setSelectionDimensions1] = useState({});
    const [selectionDimensions2, setSelectionDimensions2] = useState({});

    const [startPoint, setStartPoint] = useState(null);
    const [groupName, setGroupName] = useState(""); // state for groupName
    const [schoolName, setSchoolName] = useState(""); // state for schoolName
    const [currentSelection, setCurrentSelection] = useState(null);
    const isDrawing = useRef(false);
    const location = useLocation();
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const navigate = useNavigate();
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === "r" && currentSelection) {
                setSelectionDimensions1({ ...currentSelection, videoIndex: currentVideoIndex });
                console.log(selectionDimensions1)
                alert("Dimensions saved in selection 1");
            }
    
            if (e.key === "c" && currentSelection) {
                setSelectionDimensions2({ ...currentSelection, videoIndex: currentVideoIndex });
                console.log(selectionDimensions2)
                alert("Dimensions saved in selection 2");
            }
        };
    
        document.addEventListener("keydown", handleKeyDown);
        return () => {
            document.removeEventListener("keydown", handleKeyDown);
        };
    }, [currentSelection, currentVideoIndex]);

    const handleVideoUpload = (event) => {
        resetState(); // Reset state before adding new videos
        const files = Array.from(event.target.files);
        const newVideos = files.map(file => ({
            file: URL.createObjectURL(file),
            blob: file
        }));
        setVideos(newVideos);
    };


    const extractFrame = () => {
        if (!videoRef.current) return;
        videoRef.current.src = videos[currentVideoIndex].file;
        videoRef.current.onloadedmetadata = () => {
            const video = videoRef.current;
            canvasRef.current.width = video.videoWidth;
            canvasRef.current.height = video.videoHeight;
            drawInitialFrame();

            video.currentTime = 3.33; // Assuming 30 fps
        };
    };

    const drawInitialFrame = () => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        const video = videoRef.current;
        if (canvas && video) {
            // Only draw the image without clearing the canvas
            context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
        }
    
    };

    const drawSelection = () => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        if (!currentSelection || !canvas) return;
    
        // Clear the previous drawing
        context.clearRect(0, 0, canvas.width, canvas.height);
        // Redraw the initial frame so the video frame is still visible after clearing
        drawInitialFrame();
        
        context.beginPath();
        context.strokeStyle = 'red';
        context.lineWidth = 2;
        context.rect(
            currentSelection.x1, currentSelection.y1,
            currentSelection.x2 - currentSelection.x1,
            currentSelection.y2 - currentSelection.y1
        );
        context.stroke();
    };
    

    const handleMouseDown = (e) => {
        const rect = canvasRef.current.getBoundingClientRect();
        setStartPoint({
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        });
        isDrawing.current = true;
        setCurrentSelection(null);
    };

    const handleMouseMove = (e) => {
        if (!startPoint || !isDrawing.current) return;

        const rect = canvasRef.current.getBoundingClientRect();
        const newSelection = {
            x1: startPoint.x,
            y1: startPoint.y,
            x2: e.clientX - rect.left,
            y2: e.clientY - rect.top
        };
        setCurrentSelection(newSelection);
        drawSelection();
    };
    
    const handleMouseUp = () => {
        isDrawing.current = false;
        if (currentSelection) {
            const updatedSelections = { ...selections, [currentVideoIndex]: currentSelection };
            setSelections(updatedSelections);
        }
    };
    
    
    const handleUpload = async () => {
        if (!videos.length) {
            alert("Please select a video to upload.");
            return;
        }
    
        if (!selectionDimensions1 || !selectionDimensions2) {
            alert("Please select both ROI dimensions.");
            return;
        }
    
        if (groupName.trim() === "") {
            alert("Group name cannot be empty.");
            return;
        }
    
        // Show a loading alert
        const loadingAlert = Swal.fire({
            title: 'Uploading...',
            showConfirmButton: false,
            buttonsStyling: false,
            text: 'Please wait while the video is uploaded and processed.',
            allowOutsideClick: false,
            onBeforeOpen: () => {
                Swal.showLoading();
            },
        });
    
        try {
            const formData = new FormData();
            formData.append('video', videos[0].blob);
            formData.append('selection1', JSON.stringify(selectionDimensions1));
            formData.append('selection2', JSON.stringify(selectionDimensions2));
            formData.append('groupName', groupName); // Add groupName to the FormData
    
            const response = await fetch('http://127.0.0.1:5000/video-upload', {
                method: 'POST',
                body: formData,
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log(data);
    
            if (data.message === "error") {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error in uploading video, please refresh and try again.',
                    buttonsStyling: false,
                });
            } else if (data.message === "ok") {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Video uploaded and processed successfully.',
                    buttonsStyling: false,
                });
            }
        } catch (error) {
            console.error('Error during the file upload:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error during the file upload. Please try again later.',
                buttonsStyling: false,
            });
        } finally {
            // Close the loading alert
            loadingAlert.close();
        }
    };
    const resetState = () => {
        setVideos([]);
        setCurrentVideoIndex(0);
        setSelections({});
        setSelectionDimensions1({});
        setSelectionDimensions2({});
        setStartPoint(null);
        setGroupName("");
        setSchoolName("");
        setCurrentSelection(null);
        isDrawing.current = false;
    };

    const handleDone = () => {
        navigate('/selectframes', { state: { schoolName: schoolName, groupName: groupName } });
    }
    
    const sendData = async (video, selection) => {
        const formData = new FormData();
        formData.append('video', video.blob);
        formData.append('selection1', JSON.stringify(selectionDimensions1));
        formData.append('selection2', JSON.stringify(selectionDimensions2));
        console.log("SENDING")
    
        try {
            const response = await fetch('http://127.0.0.1:5000/video-upload', {
                method: 'POST',
                body: formData,
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log(data);
            if(data.message==="error"){
                alert("Error in uploading video, please refresh and try again")
            }
            if(data.message==="ok"){
                alert("Video uploaded and processed successfully")
            }
        } catch (error) {
            console.error('Error during the file upload:', error);
        }
    };
    const handleGroupNameChange = (event) => {
        setGroupName(event.target.value);
    };
    
    useEffect(() => {
        if (location.state && location.state.schoolName) {
            setSchoolName(location.state.schoolName);
        } else {
            alert("Please login before entering this page");
            navigate('/');
        }

        if (videos.length > 0) {
            extractFrame();
        }
    }, [currentVideoIndex, videos]);
    
    return (
        <div>
            <h1 className={styles.heading}>Classification Interface</h1>
            <input
                type="text"
                placeholder="Enter group name"
                value={groupName}
                onChange={handleGroupNameChange}
                className={styles.textInput}
            />
            <br></br>
            <input
                type="file"
                accept="video/*"
                multiple
                onChange={handleVideoUpload}
                className={styles.uploadInput}
            />
            {videos.length > 0 && (
                <div>
                    <video
                        ref={videoRef}
                        style={{ display: "none" }}
                        onSeeked={drawInitialFrame}
                    ></video>
                    <canvas
                        ref={canvasRef}
                        style={{ cursor: 'crosshair' }}
                        onMouseDown={handleMouseDown}
                        onMouseMove={handleMouseMove}
                        onMouseUp={handleMouseUp}
                    />
                    {/* <button onClick={handleNextVideo}>Next Video</button> */}
                </div>
            )}
            <br></br>
            <button className={styles.button} onClick={handleUpload}>Upload</button>
            <br></br>
            <br></br>
            <button className={styles.button} onClick={handleDone}>Done</button>
        </div>
    );
            }
            
            export default AdminInterface;
