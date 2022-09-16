import React, { useState, useEffect } from "react";
import useHttp from "../hooks/use-http";
import BreadCrumbs from "../util/components/BreadCrumbs";
import useAlert from "../hooks/use-alert"
import SetAlert from "../util/components/SetAlert";
import tracklogo from '../images/track.png';

const TracksPage = () => {
  const [tracks, setTracks] = useState([]);
  const list = ["Home", "Certification Tracks"];
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  
  useEffect(() => {
    sendRequest({ url: `/courses/tracks/` }, setTracks).catch(() => {});
  }, [sendRequest]);

  const trackMap = {
    what: (sname) => `What is ${sname} Certification?`,
    why: (sname) => `Why ${sname} Certification?`,
    who: (sname) => `Who earns ${sname} Certification?`,
    benefits: () => "Benifits",
    how: (sname) => `How to become ${sname} Certified?`,
    requirements: () => "General Requirements",
    maintainance: () => "Maintain your Certification",
  };

  return (
    <>
      <BreadCrumbs list={list} title="Certification Tracks" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <div className="container p-3">
        <p>
          POLICE TECHNICAL certification tracks are comprised of 5 POLICE
          TECHNICAL classNamees, totaling 80 hours of training. To achieve
          Certification, candidates must successfully complete the
          <strong>primary course</strong>, and
          <strong>four supporting core courses</strong>.<br />
          <br />
          Courses vary from track to track and may be taken in any order, within
          2 years of completing the first className. Certification Track
          Candidates must achieve 80% or higher on all post-course examinations.
          <br />
          <br />
          <strong>Agencies</strong> interested in Certifying their personnel are
          encouraged to Become a Host, to begin the Certification Process. You
          will be contacted by a Training Coordinator to discuss group pricing
          and scheduling.
          <br />
          <br />
          <strong>Individual Officers and Support Personnel</strong> wishing to
          be certified are encouraged to email
          <a href="mailto:training@policetechnical.com">
            training@policetechnical.com
          </a>
          to speak with a Training Coordinator about individual pricing and
          scheduling.
        </p>

        <div className="accordion" id="tracks">
          {tracks.map((track, i) => (
            <div className="accordion-item" key={i}>
              <h2 className="accordion-header" id={`$heading{track.id}`}>
                <button
                  className="accordion-button"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target={`#collapse${track.id}`}
                  
                  aria-expanded={i === 0 ? true : false}
                  aria-controls={`collapse${track.id}`}
                >
                  <h5>{track.title}</h5>
                  <div className="row">
                    <div className="col-sm-5 m-auto">
                      <img src={tracklogo} className="img-fluid" alt="alt" />
                    </div>
                  </div>
                </button>
              </h2>
              <div
                id={`collapse${track.id}`}
                className={`accordion-collapse collapse ${
                  i === 0 ? "show" : ""
                }`}
                aria-labelledby={`$heading{track.id}`}
                data-bs-parent="#tracks"
              >
                <div className="accordion-body">
                  {Object.keys(trackMap).map((key,i) => (
                    <div className="row" key={i}>
                      <div className="col">
                        <p>
                          <strong>{trackMap[key](track.shortName)}</strong>
                        </p>
                        {Array.isArray(track[key]) ? (
                          <ul>
                            {track[key].map((li,i) => (
                              <li key={i}>{li}</li>
                            ))}
                          </ul>
                        ) : (
                          <p>{track[key]}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
           {tracks.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Tracks Available</h4>
            </div>
          )}
        </div>

        <br />
        <div className="row"></div>
      </div>
    </>
  );
};

export default TracksPage;
