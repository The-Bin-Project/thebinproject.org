import React from 'react';
import styles from './Navbar.module.css';

import logo from '../assets/logo.png'; 

const Navbar = () => {
  const handleScroll = (selector) => {
    const element = document.querySelector(selector);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className={styles.navbar}>
      <div className={styles.navbarLeft}>
        <img src={logo} alt="Project Bin Logo" className={styles.navbarLogo} onClick={() => { handleScroll('#pbin'); }} />
        <a href="#pbin" onClick={(e) => { e.preventDefault(); handleScroll('#pbin'); }}>Project Bin</a>
      </div>
      <div className={styles.navbarRight}>
        <a href="#idea" onClick={(e) => { e.preventDefault(); handleScroll('#idea'); }}>The Idea</a>
        <a href="#cwork" onClick={(e) => { e.preventDefault(); handleScroll('#cwork'); }}>Current Work</a>
        <a href="##login" onClick={(e) => { e.preventDefault(); handleScroll('#login'); }}> Login</a>
      </div>
    </div>
  );
};

export default Navbar;
