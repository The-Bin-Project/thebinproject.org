import React from 'react';
import './Foodfacts.css';

const Foodfacts = (props) => {
    return (
        <div className="fact-card" style={{ backgroundColor: props.colour }}>
            <h2 className="fact-title">{props.name}</h2>
            <p className="fact-text">{props.text}</p>
        </div>
    );
}

export default Foodfacts;
