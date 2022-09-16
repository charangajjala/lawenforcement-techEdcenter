import React from "react";
import mp4video from "../media/gps_tracking.mp4";
import oggvideo from "../media/gps_tracking.ogg";
import fallbackimg from "../images/gps_tracking_fallback.jpg";

const Home = () => {
  const styles = {
    width: "100%",
    height: "100%",
    position: "absolute",
    /*  top: 0,
    left: 0, */
    zIndex: 2,
    backgroundColor: "rgba(0,112,192,.3)",
  };

  return (
    <div>
      <div style={styles}></div>
      <img src={fallbackimg} alt="Loading" />
      {/*  <video autoPlay muted >
        <source src={mp4video} poster={fallbackimg} type="video/mp4" />
        <source src={oggvideo} poster={fallbackimg} type="video/ogg" />
      </video> */}
    </div>
  );
};

export default Home;
