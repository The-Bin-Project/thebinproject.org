import React from 'react';
import styles from './Navbar.module.css';

const Navbar = () => {
  return (
    <div className={styles.navbar}>
      <div className={styles.navbarLeft}>
		<a href="#pbin">Project Bin</a>
      </div>
      <div className={styles.navbarRight}>
		<a href="#idea">The Idea</a>
		<a href="#team">The Team</a>
      </div>
    </div>
  );
};

export default Navbar;
