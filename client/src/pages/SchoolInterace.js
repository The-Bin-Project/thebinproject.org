import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; 
import styles from './SchoolInterface.module.css';
import MenuTable from '../components/MenuTable';

function SchoolInterface() {
    const navigate = useNavigate();
    const location = useLocation();
    const [groups, setGroups] = useState([]);
    const [schoolName, setSchoolName] = useState('');

    // Function to navigate to admin
    const goToAdmin = () => {
        navigate('/admin', { state: { schoolName: schoolName } });
    };

    useEffect(() => {
        // Get the school name from the previous page
        try {
            const username = location.state.schoolName;
            setSchoolName(username);
        } catch (err) {
            alert("Please login before entering this page");
            navigate('/');
        }
    }, [location.state.schoolName, navigate]);

    useEffect(() => {
        if (schoolName) {
            fetchData();
        }
    }, [schoolName]); // Run this effect when schoolName changes

    async function fetchData() {
        try {
            const response = await fetch(process.env.REACT_APP_BACKEND + '/get-groups', {
                method: 'POST',
                body: JSON.stringify({ schoolName: schoolName }),
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setGroups(data.groups); // Assuming the response contains a 'groups' field
        } catch (error) {
            console.error('Failed to fetch groups:', error);
        }
    }

    // Function to handle group button click
    const handleGroupClick = (groupName) => {
        // Perform action on group click, e.g., navigate to group's page
        console.log(groupName);
        navigate('/group-page', { state: { groupName: groupName ,schoolName:schoolName} });
    };

    return (
        <div>
            <h1 className={styles.heading}> Welcome {schoolName}</h1>
            <p className={styles.paragraph}>Thank you for being a part of Project Bin! This is your school's user interface. To classify a new set of data please click "Add a new group" and upload the relevant videos. Please ensure that the menu you provide for each day is as accurate as possible to maximise the accuracy of the classifcation.</p>
            <p className={styles.paragraph}>My Groups</p>
            <br/>
            {groups.map((group, index) => (
                <button 
                    key={index} 
                    className={styles.groupButton} 
                    onClick={() => handleGroupClick(group)}>
                    {group}
                </button>
            ))}
            <br></br>
            <button className={styles.button} onClick={goToAdmin}>Add New Group</button>
            <br/>

            {/* Render buttons for each group */}
            

            <MenuTable schoolName={schoolName}/>
        </div>
    );
}

export default SchoolInterface;
