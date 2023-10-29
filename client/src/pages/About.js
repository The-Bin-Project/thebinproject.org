import React from 'react';
import styles from './About.module.css';
import Testimonials from '../components/Testimonials';

function About() {
  return (
    <div id="team">
      <section className={styles.hero1}>
        <br></br>
        <br></br>
        <div className={styles.container1}>
          <div className={styles.leftCol1}>
            <h1 className={styles.heading1}>About Us</h1>
          </div>
        </div>
        <div className={styles.testemonialContainer}>
          <Testimonials name="Aditya Agrawal" text={`"Project Bin resonates with my values of sustainable living. Beyond reducing food wastage, it's a versatile and robust solution scalable for wider impact. With increased modules, data-driven accuracy improves, potentially modeling food wastage behaviors. This endeavor has allowed me to use my skills for positive change, bringing me immense satisfaction."`}/>
          <Testimonials name="Hanming Ye" text={`"The interdisciplinary nature of our project uniquely addresses food waste, with technology, economics, and education interwoven. Our diverse team is backed by a network of experts, ensuring our initiative's resilience. Challenges arise, but our shared vision and growth mindset drive us forward, aiming to implement the Bin system across Singapore."`}/>
          <Testimonials name="Anika Sharma" text={`"Food waste is concerning in Singapore. Project Bin's unique approach helps reduce waste, benefiting both the environment and finances. Its scalability is a standout feature. Through collaboration, I've enhanced my systems thinking and realized technology's power in addressing humanitarian issues like food wastage."`}/>
          <Testimonials name="Antoine Lee" text={`"I stand by Project Bin for its vision and potential societal impact. Tackling plate waste is our unique angle, different from existing solutions focusing on catering waste. This multidisciplinary project goes beyond traditional subjects, integrating AI and behavioral economics. Through this, I've appreciated teamwork and the integration of diverse skill sets."`}/>
        </div>
      </section>
    </div>
  );
}

export default About;
