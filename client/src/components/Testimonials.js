import React from 'react';
import './Testimonials.css';

const Testimonials = (props) => {
    return (
        <div className="testimonial-card">
            <h2 className="testimonial-title">{props.name}</h2>
            <p className="testimonial-text">{props.text}</p>
        </div>
    );
}

export default Testimonials;
