import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Navbar.module.css';

const Navbar = () => {
  return (
    <div className={styles.navbar}>
      <div className={styles.navbarLeft}>
        <Link to="/">Project Bin</Link>
      </div>
      <div className={styles.navbarRight}>
        <Link to="/idea">The Idea</Link>
        <Link to="/about">The Team</Link>
        <Link to="/reports">Current Work</Link>
      </div>
    </div>
  );
};

export default Navbar;
