import React from "react";
import styles from "./Idea.module.css";
import videoSrc from "../assets/vidIdea.mp4"; 
import classVideo from "../assets/classification.mp4";
import binpic1 from "../assets/binpic1.png";
import binpic2 from "../assets/binpic2.jpg";

function Idea() {
    return (
        <div id="idea">
            <section className={styles.idea}>
                <h1 className={styles.heading2}>The Idea</h1>
                <div className={styles.ideaContainer}>
                    <div className={styles.whiteCard}>
                        <h1 className={styles.title}>Reducing Food Waste in School Canteens</h1>
                        <p className={styles.ideaText}>We aim to minimise food waste in Singapore’s 180 schools and 115 hawkers through data analytics and behavioural economics</p>
                        <p className={styles.ideaText}><span className={styles.boldText}>Our Solution is:</span></p>
                        <p className={styles.ideaText}>1) <span className={styles.boldText}>Track and classify </span> consumer plate waste by stationing cameras with <span className={styles.boldText}>AI object recognition</span> on bins.</p>
                        <p className={styles.ideaText}>2) Use <span className={styles.boldText}> data analysis </span> to find underlying causes behind behavioural patterns and wastage trends.</p>
                        <p className={styles.ideaText}>3) Work with kitchens to implement changes that address these underlying causes. Drawing from <span className={styles.boldText}>behavioural economics</span>, we create nudges that change consumer choices.</p>
                        <p className={styles.ideaText}>4) Publish findings to consumers via <span className={styles.boldText}>reports and interactive platforms.</span></p>
                        <p className={styles.ideaText}>By reducing costs for food vendors and educating consumers about their underlying habits, we tie key stakeholders together, and work together to solve the multifaceted issue of food waste. And by designing our system to be replicable, we seek to create a network of bin systems across cafeterias islandwide. This way, we can tackle food waste one bin at a time.</p>
                    </div>
                    <video className={styles.videoPop} autoPlay loop muted>
                        <source src={videoSrc} type="video/mp4" />
                    </video>
                </div>
            </section>
            <section>
                <h1 className={styles.heading2}>The Technology</h1>
                <div className={styles.ideaContainer}>
                    <div className={styles.whiteCard}>
                        <h1 className={styles.title}>The Stack</h1>
                        <p className={styles.ideaText}>
                            Currently, our team is immersed in the meticulous process of collating and labelling data to increase the accuracy of our machine learning model. This labelling process adds another layer of accuracy as it increases the scope of the types of dishes the model can recognise, increasing specificity further.
                        </p>
                        <p className={styles.ideaText}>
                            We have opted for the YOLO (You Only Look Once) v7 model to drive the classification task in our project. YOLO v7 is a cutting-edge real-time object detection system known for its speed and accuracy. By training YOLO v7 on our labelled dataset, we aim to develop a robust model capable of classifying waste into predefined categories (e.g., Pad Thai Noodles, fried rice). Through continuous iteration, evaluation, and possibly augmenting our dataset further, we aspire to fine-tune our model to achieve greater accuracy in waste classification.
                        </p>
                    </div>
                    <video className={styles.videoPop} autoPlay loop muted>
                        <source src={classVideo} type="video/mp4" />
                    </video>
                </div>
                {/* <img src={binpic1} alt="Bin Picture 1" className={styles.binImage} />
                <img src={binpic2} alt="Bin Picture 2" className={styles.binImage} /> */}
            </section>
        </div>
    );
}

export default Idea;
