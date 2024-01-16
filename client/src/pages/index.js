import React, { useEffect, useRef } from "react";

const pageStyles = {
    color: "#232129",
    padding: 96,
    fontFamily: "-apple-system, Roboto, sans-serif, serif",
};
const headingStyles = {
    marginTop: 0,
    marginBottom: 64,
    maxWidth: 320,
};

const IndexPage = () => 
{
    const imageRef = useRef(null);
	
	const formatResponse = (foodData) => {
		let res = ''
		Object.keys(foodData).forEach(item => {
			if (item != 'EMPTY') { res += item + ': ' + foodData[item] + '\n' }
		})
		return res
	}

    useEffect(() => {
		const listElement = document.getElementById('list');
        const ws = new WebSocket('ws://localhost:8765');
    
        ws.onopen = () => {
            console.log('Connected to the WebSocket server.');
        }
    
        ws.binaryType = 'blob';

        ws.onmessage = function(event) {
		        const blob = event.data;
                const objectData = JSON.parse(blob);
				const base64data = objectData.image;
                const data = 'data:image/jpeg;base64,' + base64data;
                imageRef.current.src = data;
				console.log(objectData.data.data)
				listElement.innerHTML = formatResponse(objectData.data.data);
        };
    
        ws.onerror = (error) => {
            console.error('WebSocket Error: ', error);
        };
    
        ws.onclose = (event) => {
            if (event.wasClean) {
                console.log(`Closed cleanly, code=${event.code}, reason=${event.reason}`);
            } else {
                console.error(`Connection died`);
            }
        };
    
        return () => {
            ws.close();
        }
    }, []); 


    return (
        <main style={pageStyles}>
            <h1 style={headingStyles}>BOBOT</h1>
            <h2>Image</h2>
            <img ref={imageRef} />
			<h3 id='list'></h3>
			<canvas id="pieChart" />
        </main>
    );
};

export default IndexPage;
