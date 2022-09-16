import React, { useState, useEffect, useRef, useMemo } from "react";
import BreadCrumbs from "../util/components/BreadCrumbs";
import useHttp from "../hooks/use-http";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";

export const InstructorDescription = ({ instructor }) => {
  return (
    <div
      className="row rounded my-3"
      style={{ maxHheight: "320px", overflow: "hidden" }}
    >
      <div className="col-sm-3" style={{ maxHeight: "inherit" }}>
        <img
          src={instructor.image}
          className="img-fluid rounded"
          alt="Loading..."
        />
      </div>
      <div
        className="col-sm-9 border rounded py-1"
        style={{ maxHeight: "inherit" }}
      >
        <strong>{`${instructor.firstName} ${instructor.lastName}`}</strong>
        <p>{instructor.bio}</p>
      </div>
    </div>
  );
};

const InstructorsPage = () => {
  const [instructors, setInstructors] = useState([]);
  const list = ["Home", "Instructors"];
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest({ url: "/instructors/team/" }, setInstructors).catch(
      (err) => {}
    );
  }, [sendRequest]);

  return (
    <div>
      <BreadCrumbs list={list} title="Team" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />

      <div className="container">
        <p>
          POLICE TECHNICAL National Instructors represent the best technical
          instructors in the Field of Law Enforcement. Each of our instructors
          was chosen from hundreds of applicants in a multi-level hiring
          process; 95% of our personnel are sworn, active law enforcement, many
          with Federal and State agencies. Our instructors were chosen for their
          expertise within their subject area, their approachability, and their
          proven interest in serving fellow members of law enforcement. If you
          would like to join POLICE TECHNICAL, click here to join our mailing
          list.
        </p>
        <br />
        {instructors.map((instructor,i) => {
          return <InstructorDescription instructor={instructor} key={i} />;
        })}
         {instructors.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Instructors Available</h4>
            </div>
          )}
      </div>
    </div>
  );
};

export default InstructorsPage;
