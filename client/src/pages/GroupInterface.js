import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; 
import styles from './GroupInterface.module.css';
import { Bar,Pie,Line } from 'react-chartjs-2';
import Swal from 'sweetalert2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    LineElement,
    PointElement
  } from 'chart.js';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

function GroupInterface() {
    const navigate = useNavigate();
    const location = useLocation();
    const [schoolName, setSchoolName] = useState('');
    const [group, setGroup] = useState('');
    const [reportData, setReportData] = useState(''); // State to store report data
    const [groupData, setGroupData] = useState(null); // New state for storing response
    useEffect(() => {
        async function fetchData() {
            if (schoolName && group) {
                // Show loading alert
                Swal.fire({
                    title: 'Loading...',
                    buttonStyling: false,
                    text: 'Please wait while we fetch the data',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading();
                    },
                });
        
                try {
                    const response = await fetch(process.env.REACT_APP_BACKEND + '/get-results', {
                        method: 'POST',
                        body: JSON.stringify({ schoolName: schoolName, groupName: group }),
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });
        
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
        
                    const data = await response.json();
                    setGroupData(data.results);
        
                    // Close the loading alert
                    Swal.close();
        
                } catch (error) {
                    console.error('Failed to fetch group data:', error);
        
                    // Show error alert
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        buttonsStyling: false,
                        text: 'Something went wrong!',
                    });
                }
            }
        }
    
        fetchData(); // Call the function to fetch data
    }, [schoolName, group, navigate]); // Depend on schoolName and group

    useEffect(() => {
        try {
            const username = location.state.schoolName;
            const groupName = location.state.groupName;
            setSchoolName(username);
            setGroup(groupName);
        }
        catch (err) {
            alert("Please login before entering this page");
            navigate('/');
        }
    }   , []); // Depend on groupData
    

    

    const filteredGroupData = groupData ? groupData.filter(item => item.name !== 'Clean Plate') : [];
    console.log(filteredGroupData);

    const chartData = groupData ? {
        labels: groupData.map(item => item.name),
        datasets: [{
            label: 'Percentage of Food Wasted (without empty plates)',
            data: groupData.map(item => item.percentage_without_empty * 100),
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
        }],
    } : null;

    const pieChartData = filteredGroupData.length > 0 ? {
        labels: filteredGroupData.map(item => item.name),
        datasets: [{
            label: 'Percentage of Each Food Wasted',
            data: filteredGroupData.map(item => item.percentage * 100),
            backgroundColor: filteredGroupData.map((_, index) => `hsl(${index * 360 / filteredGroupData.length}, 70%, 60%)`),
        }],
    } : null;
    
    const lineChartData = filteredGroupData.length > 0 ? {
        labels: filteredGroupData.map(item => item.name),
        datasets: [{
            label: 'Quantity of Each Food',
            data: filteredGroupData.map(item => item.quantity),
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    } : null;

    const chartOptions = {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    const generateReport = () => {
        // Show loading alert
        Swal.fire({
            title: 'Generating Report...',
            buttonStyling: false,
            text: 'Please wait while we generate the report',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            },
        });
    
        // Make the POST request to generate the report
        fetch(process.env.REACT_APP_BACKEND + '/generate_report', {
            method: 'POST',
            body: JSON.stringify({
                groupName: group,
                schoolName: schoolName,
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setReportData(data.report[group]); // Assuming 'data.report' is the text you want to display
    
                // Close the loading alert
                Swal.close();
            })
            .catch((error) => {
                console.error('Failed to generate report:', error);
    
                // Show error alert
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    buttonsStyling: false,
                    text: 'Something went wrong while generating the report!',
                });
            });
    };

    return (
        <div>
            <h1 className={styles.heading}> Welcome {schoolName}</h1>
            <p className={styles.paragraph}>This page shows some information and analysis about the group you selected.</p>
            <p className={styles.paragraph}>Group: {group}</p>
            <button className={styles.button} onClick={generateReport}>Generate Report</button>
              
            {/* Text Box or Div to display the report data */}
            {reportData && (
                <textarea className={styles.reportBox} value={reportData} readOnly />
            )}
            
                   {/* Charts Container */}
        <div className={styles.chartsContainer}>
            {/* Render Bar Chart */}
            {groupData && (
                <div className={styles.Chart}>
                    <Bar data={chartData} options={chartOptions} />
                </div>
            )}

            {/* Render Line Chart */}
            {filteredGroupData.length > 0 && (
                <div className={styles.Chart}>
                    <Line data={lineChartData} options={chartOptions} />
                </div>
            )}

               {/* Render Pie Chart */}
               {filteredGroupData.length > 0 && (
                <div className={styles.Chart}>
                    <Pie data={pieChartData} />
                </div>
            )}

        </div>

            <br/>
        </div>
    );
}

export default GroupInterface;