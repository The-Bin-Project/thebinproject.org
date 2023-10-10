import React from 'react';
import classes from './Navbar.module.css';

const Navbar = () => {
    return (
        <nav className={classes.navbar}>
            <h3 className={classes.title}>The Bin Project</h3>
            <div className={classes.buttons}>
                <button>Landing</button>
                <button>The Idea</button>
                <button>About Us</button>
                <button>Reports</button>
            </div>
        </nav>
    );
};

export default Navbar;
