import React, { useEffect, useState } from 'react';
import styles from './MenuTable.module.css';

function MenuTable(props) {
    const [data, setData] = useState({});
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchMenu = async () => {
            setIsLoading(true);
            try {
                const response = await fetch(process.env.REACT_APP_BACKEND + '/fetch-menu', {
                    method: 'POST',
                    body: JSON.stringify({ username: props.schoolName }),
                    headers: { 'Content-Type': 'application/json' },
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const current_menu = await response.json();
                setData(current_menu.menu || {});
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            } finally {
                setIsLoading(false);
            }
        };

        if (props.schoolName) {
            fetchMenu();
        }
    }, [props.schoolName]);

    const handleChange = (day, value) => {
        setData({ ...data, [day]: value });
    };
    
    const updateDB = () => {
        // write a post request to backend with the table informatoin
        console.log(data);
        fetch(process.env.REACT_APP_BACKEND + '/update-menu', {
            method: 'POST',
            body:JSON.stringify({
                menu:data,
                username:props.schoolName}),
            headers: {
                'Content-Type': 'application/json', // Ensure you're sending the data as JSON
            },
        })
    }

    if (isLoading) {
        return <div>Loading...</div>; // Simple loading text, can be replaced with a loading spinner or similar
    }
    return (
        <div>
            <table className={styles.editableTable}>
                <thead>
                    <tr>
                        <th>Day</th>
                        <th>Dishes Served</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.keys(data).map(day => (
                        <tr key={day}>
                            <td>{day}</td>
                            <td>
                                <input 
                                    type="text"
                                    value={data[day]}
                                    onChange={(e) => handleChange(day, e.target.value)}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <br></br>
            <button className={styles.button} onClick={updateDB}>Update Menu</button>
        </div>
    );
}

export default MenuTable;