import React from 'react';
import Navbar from '../components/Navbar';
import styles from './About.module.css';
import Testimonials from '../components/Testimonials';

function About() {
  return (
    <div>
      <Navbar />
      <section className={styles.hero1}>
      <br></br>
      <br></br>
        <div className={styles.container1}>
          <div className={styles.leftCol1}>
            <h1 className={styles.heading1}>About Us</h1>
            <div className={styles.heroCta1}>
            </div>
          </div>
        </div>
      </section>
      <Testimonials name="Hanming Ye" text="The interdisciplinary nature of the project stands out most to me. We combine technology, behavioural economics, entrepreneurship, and public education to create a sustainable system. This multifaceted initiative suits the complex issue of food waste: each branch of the project helps cover for the weaknesses of the other, thereby creating a resilient movement that can withstand challenges. Behind this project is an equally diverse team, including a range of personalities, passions and perspectives. In addition, we are supported by an extensive network of experts, from teachers to kitchen managers. As our initiative grows and incorporates an increasing number of stakeholders, it becomes more stable and accepted in the wider community. With our commitment, the Bin project will steadily create visible, tangible differences. On this journey, I realised the importance of morale. Sometimes, when we get bogged down by communication with kitchens or a glitch in our code, it becomes easy to lose confidence. We discovered that during these moments, we must hold on to our original vision: implementing the Bin system across Singapore. From experience, we learnt that a growth mindset is as productive as a good plan. Moving forward, we will remain motivated to achieve our shared goal."/>
      <Testimonials name="Anika Sharma" text="To me, food waste in Singapore has always been an area of concern. I think that this idea stands out because of the unique approach it takes in combating a widespread issue. Project Bin provides a simple yet useful strategy for organisations and canteens to reduce the waste produced hence both benefiting the environment, as well as saving money. However, perhaps what is most notable about this proposal is its highly scalable nature. After being implemented in a local setting, the technology used can very easily be expanded to other locations hence accelerating the impact it makes. I think that ultimately, this project is a feasible and innovative initiative which informs canteens and organisations of the food being wasted - and this knowledge allows for great possibility for change. Through this project, I’ve not only learnt to collaborate effectively with people with various expertises, but also heightened my systems thinking and critical evaluation skills when ideating and researching. Apart from the learning from an academic and technical perspective, I’ve also gained a series of rewarding experiences and been able to see the significance and the impact technology can make in solving humanitarian issues - such as food waste."/>
      <Testimonials name="Aditya Agrawal" text="Project Bin reflects my core principles and values of sustainable living and reducing our carbon footprint. It hurts me to see food wastage when many stomachs go hungry and  resources are invested into its production. It’s an innovative solution to minimise food wastage, save resources, bring awareness, and enact a positive change. Project Bin distinguishes itself from other proposals in its versatility and robustness that facilitate scalability and rapid deployment. Additionally, as the number of modules in operation increases, accuracy will be enhanced, helped by more comprehensive data gathered. These two properties lead me to believe that Project Bin will provide an effective solution to the issue of food waste. The insights provided from such an amalgamation of data may also prove to be an invaluable resource for modelling various food wastage phenomena; particularly, when considering the habitual and routine nature of our eating habits. Working on this project has given me the opportunity to harness my skillset and gain the confidence to use it as a medium to bring about a positive change. To see the project develop and bear fruit has brought me joy and satisfaction"/>
      <Testimonials name="Antoine Lee" text="I believe in Project Bin because of our shared vision, as well as the tangible impact it will have on society. When food is discarded, resources are being wasted, while simultaneously contributing towards the detrimental global issue of climate change. I believe that our innovative solution to the humanitarian issue of food wastage, and our unique angle of tackling consumer plate waste as opposed to focusing on catering waste like existing solutions, will really make a difference. In this team, I hope to further pursue my passion for programming and make an impact. My belief in this project extends beyond its idea and impact, but also our team and the process of working on it. Something I really appreciate is the multidisciplinary nature of the project; how it extends past the confines of classroom mathematics and towards intriguing topics such as artificial intelligence or behavioural economics. Problem solving was a particularly important part of the process, as there are so many different aspects and technologies we are combining when bringing this idea to life. Through working on this project, I have learned the value of teamwork, and how to work closely with my teammates to integrate our various skill sets."/>
    </div>
  );
}

export default About;
