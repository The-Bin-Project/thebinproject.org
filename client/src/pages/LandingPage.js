import React from 'react';
import classes from './LandingPage.module.css'

import progressVid from '../assets/progressVid.mp4';

import aboutUs from '../assets/aboutUs.jpg';

// 1) landing 2) the idea 3) about us 4) reports

function LandingPage() {
    return (
        <div>
            <section className={classes.coverContainer}>
                <h1>The Bin Project</h1>
                <h2>A UWCSEA East Initiative</h2>
            </section>
            <section className={classes.ideaContainer}>
                <h2>The Idea</h2>
                {/* <video className={classes.ideaVid}>
                    <source src={ideaVid} type="video/mp4" />
                    Your browser does not support the video tag.
                </video> */}
                {/* play this yt vid: https://www.youtube.com/watch?v=V-9scTKF7PU */}
                {/* <video className={classes.ideaVid}>
                    <source src="https://www.youtube.com/watch?v=V-9scTKF7PU" type="video/mp4" />
                    Your browser does not support the video tag.
                </video> */}
                <iframe src="https://www.youtube.com/embed/V-9scTKF7PU?autoplay=1&mute=1"></iframe>
                <p>We aim to minimise food waste in Singapore’s 180 schools and 115 hawkers through data analytics and behavioural economics. Our solution is to:</p>
                <ul>
                    <li><strong>Track and classify consumer plate waste</strong> by stationing cameras with AI object recognition on bins.</li>
                    <li>Use <strong>data analysis</strong> to find <strong>underlying causes</strong> behind <strong>behavioural patterns</strong> and <strong>wastage trends</strong>.</li>
                    <li>Work with kitchens to <strong>implement changes</strong> that address these underlying causes. Drawing from behavioural economics, we create nudges that change consumer choices. </li>
                    <li>Publish findings to consumers via reports and interactive platforms.</li>
                </ul>
                <p>By reducing costs for food vendors and educating consumers about their underlying habits, we <strong>tie key stakeholders together</strong>, and work together to solve the multifaceted issue of food waste. And by designing our system to be replicable, we seek to create a <strong>network</strong> of bin systems across cafeterias islandwide. This way, we can tackle food waste one bin at a time.</p>
            </section>
            <section className={classes.progressContainer}>
                <h2>Our Progress</h2>
                <video loop autoPlay muted className={classes.progressVid}>
                    <source src={progressVid} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
                <p>Currently, our team is immersed in the meticulous process of collating and labelling data to increase the accuracy of our machine learning model. This labelling process adds another layer of accuracy as it increases the scope of the types of dishes the model can recognise, increasing specificity further.</p>
                <p>We have opted for the YOLO (You Only Look Once) v7 model to drive the classification task in our project. YOLO v7 is a cutting-edge real-time object detection system known for its speed and accuracy. By training YOLO v7 on our labelled dataset, we aim to develop a robust model capable of classifying waste into predefined categories(eg. Pad Thai Noodles,  fried rice). Through continuous iteration, evaluation, and possibly augmenting our dataset further, we aspire to fine-tune our model to achieve greater accuracy in waste classification.</p>
            </section>
            <section className={classes.aboutContainer}>
                <h2>About Us</h2>
                <img src={aboutUs} alt="Team Pic" />
                <p>We are a group of students studying at UWCSEA East aiming to use technology to address real world problems — such as preventing food waste in schools.</p>
                <h3>Our Team</h3>
                <div className={classes.bioContainer}>
                    <div className={classes.bio}>
                        <h4>Hanming Ye</h4>
                        <p>"Embracing a multidisciplinary approach, our team tactically addresses food waste through technology and behavioral economics in the Bin project. A fusion of varied skills and perspectives amplifies our impact, ensuring resilience and community integration. Amidst challenges, our unwavering vision and growth mindset propel us toward implementing sustainable systems across Singapore."</p>
                    </div>
                    <div className={classes.bio}>
                        <h4>Anika Sharma</h4>
                        <p>"Project Bin marries technological strategy and scalable impact to tackle Singapore's food waste issue, providing organizations a practical method for reduction and awareness. My journey has enhanced my collaborative, critical thinking, and technical skills, revealing technology’s significant role in addressing humanitarian issues like food waste, and propelling feasible, innovative change."</p>
                    </div>
                    <div className={classes.bio}>
                        <h4>Aditya Agrawal</h4>
                        <p>"Aligning with my principles of sustainable living, Project Bin innovatively minimizes food wastage and spurs positive change with its scalable and data-enhanced approach. My involvement has enabled me to apply my skills towards meaningful impact, finding joy and satisfaction as the project matures and offers valuable insights into combating food wastage phenomena."</p>
                    </div>
                    <div className={classes.bio}>
                        <h4>Antoine Lee</h4>
                        <p>"Project Bin, with its unique focus on consumer plate waste, strives to make a tangible societal impact by mitigating food wastage and consequent environmental effects. I cherish the project’s multidisciplinary nature and problem-solving aspects, involving realms like AI and behavioral economics. Through active involvement, I’ve appreciated the collaborative spirit and skill integration within our team."</p>
                    </div>
                </div>
            </section>
            <section className={classes.reportsContainer}>
                <h2>Reports</h2>
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
            </section>
            <section className={classes.contactContainer}>
                <h2>Contact Us</h2>
                <p>Feel free to reach out to any of us if you have any questions, or would like to be involved in the project!</p>
                <div className={classes.contactInfo}>
                    <div className={classes.contact}>
                        <h4>Hanming Ye</h4>
                        <p>ye57324@gapps.uwcsea.edu.sg</p>
                    </div>
                    <div className={classes.contact}>
                        <h4>Anika Sharma</h4>
                        <p>sharm51155@gapps.uwcsea.edu.sg</p>
                    </div>
                    <div className={classes.contact}>
                        <h4>Aditya Agrawal</h4>
                        <p>agraw17107@gapps.uwcsea.edu.sg</p>
                    </div>
                    <div className={classes.contact}>
                        <h4>Antoine Lee</h4>
                        <p>lee12048@gapps.uwcsea.edu.sg</p>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default LandingPage;