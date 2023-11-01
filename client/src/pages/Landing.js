import React from "react";
import styles from "./Landing.module.css"; // Import styles
import { useEffect, useRef } from "react";
import Foodfacts from "../components/Foodfacts";
function Landing() {
    const infoSectionRef = useRef(null);

    return (
        <div id="pbin">
            <section className={styles.landingpic}>
                <div className={styles.container}>
                    <div className={styles.leftCol}>
                        <p className={styles.subHead}>
                            A UWCSEA East Initiative
                        </p>
                        <h1 className={styles.mainTitle}>Project Bin</h1>
                    </div>
                </div>
            </section>

            <section ref={infoSectionRef} className={styles.info}>
                <h1 className={styles.infoHeading}>Reducing Food Waste in Canteens</h1>
                <div className={styles.foodfactsGrid}>
                <Foodfacts
                        name="Food Waste Globally"
                        text="Globally, one-third of all food produced is wasted, amounting to 1.3 billion tons annually. This waste emits 8% of global greenhouse gases, exacerbating hunger and climate change."
                        colour="#E1FEEC"
                    ></Foodfacts>
                <Foodfacts
                        name="Food Waste in Canteens"
                        text="Consumer Plate Waste accounts still for the majority of wastage: 89% in our school community. Currently, targeted action is impossible as no one knows what exactly is being wasted — once it's thrown away, the waste goes out of sight out of mind."
                        colour="#E7E1F1"
                    ></Foodfacts>
                    <Foodfacts
                        name="Food Waste in Singapore"
                        text="Did you Know that there every day in Singapore, we throw away more than 2,000 tonnes? Globally over 1 billion tonnes of food is wasted. Like many developed countries, Food waste is a major concern for Singapore, both because of how it has to be managed and the resources that go into producing it."
                        colour="#E9F1E1"
                    ></Foodfacts> 
                 
                    <Foodfacts
                        name="Our Solution"
                        text="Our Solution is to address this information gap between what is being wasted and those producing it by using AI Classification to recognise the food which is being wasted and feed this information back to Canteen staff."
                        colour="#E1F1EC"
                    ></Foodfacts>
                </div>
            </section>

        </div>
    );
}

export default Landing;
