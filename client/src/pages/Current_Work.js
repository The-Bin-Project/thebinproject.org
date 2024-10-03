import React from "react";
import styles from "./Current_Work.module.css";

function Current_Work() {
    const fileId1 = '1_LsLR_db3GvtGYY-eyW7FBJGJS-VN-nE';
    const embedUrl1 = `https://drive.google.com/file/d/${fileId1}/preview`;
    const fileId2 = "1n6ify3FjifnUGnYj5uo5JGXC6vvOX9LR"
    const embedUrl2 = `https://drive.google.com/file/d/${fileId2}/preview`;
    const fileId3 = "1FdvLTA5Cht9FRU_ce3BwfQI7Yk8AtKBdZk9ClkUHHPc";
    const reportEmbedLink = 'https://drive.google.com/file/d/${fileId3}/preview';


    return (
        <div id="cwork">
            <section className={styles.reports}>
                <h1 className={styles.heading2}>Current Work</h1>
                
                <div className={styles.reportContainer}>
                    {/* First iframe */}
                    <iframe
                        src={embedUrl1}
                        allowFullScreen
                        className={styles.reportIframe}
                        title="Current Work Report"
                    >
                        <p>Your browser does not support iframes.</p>
                    </iframe>
                    
                    {/* Second iframe */}
                    <iframe
                        src={embedUrl2}
                        allowFullScreen
                        className={styles.reportIframe}
                        title="Current Work Report"
                    >
                        <p>Your browser does not support iframes.</p>
                    </iframe>
                            {/* Google Slides iframe */}
                            <iframe
                        src={reportEmbedLink}
                        allowFullScreen
                        className={styles.reportIframe}
                        title="Current Work Report"
                    >
                        <p>Your browser does not support iframes.</p>
                    </iframe>
                </div>
            </section>
        </div>
    );
}

export default Current_Work;
