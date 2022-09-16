import React, { useState, useEffect } from "react";
import ClsRow from "../../util/components/ClsRow";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import Modal from "../../util/components/Modal";

const CurrentClass = ({ current, sendRequest }) => {
  const ShowCourses = ({ courses, rem, title }) => {
    const ShowCourse = ({ courses }) => {
      return (
        <div>
          {courses &&
            courses.map((course, i) => {
              return (
                <ul key={i}>
                  <li>{course.title}</li>
                </ul>
              );
            })}
        </div>
      );
    };
    return (
      <div className="container">
        <h2>{title}</h2>
        {rem !== true ? (
          <ShowCourse courses={courses} />
        ) : (
          <div>
            <h3>Required Courses</h3>
            <ShowCourse courses={courses.required} />
            <h3>Optional Courses</h3>
            <ShowCourse courses={courses.optional} />
          </div>
        )}
      </div>
    );
  };

  return (
    <div>
      <div className="row">
        <div className="col-sm-8">
          <div className="row">
            <div className="col-sm-6">
              <table className="table table-bordered ">
                <tbody>
                  {" "}
                  <ClsRow name="Track Name" val={current.title} />
                  <ClsRow name="Short Name" val={current.shortName} />
                </tbody>
              </table>
            </div>

            <div className="col-sm-6">
              <table className="table table-bordered ">
                <tbody>
                  <ClsRow
                    name="Completed Courses"
                    val={
                      <Modal
                        mdltitle="View"
                        Component={ShowCourses}
                        props={{
                          courses: current.completedCourses,
                          title: "Completed Courses",
                          rem: false,
                        }}
                        thisModal="CompletedCourses"
                      />
                    }
                  />
                  <ClsRow
                    name="Remaining Courses"
                    val={
                      <Modal
                        mdltitle="View"
                        Component={ShowCourses}
                        props={{
                          courses: current.remainingCourses,
                          title: "Remaining Courses",
                          rem: true,
                        }}
                        thisModal="RemainingCourses"
                      />
                    }
                  />
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="col-sm-4"></div>
      </div>
    </div>
  );
};

const StudentTracks = () => {
  const [currents, setCurrents] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest({ url: "/classes/student/tracks/" }, setCurrents).catch(
      (err) => {}
    );
  }, [sendRequest]);

  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      {currents.map((current) => (
        <CurrentClass
          current={current}
          sendRequest={sendRequest}
          key={current.id}
        />
      ))}
    </div>
  );
};

export default StudentTracks;
