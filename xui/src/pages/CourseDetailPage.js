import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import useHttp from "../hooks/use-http";
import BreadCrumbs from "../util/components/BreadCrumbs";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";
import { giveProperDate } from "../util/helper-functions/util-functions";

export const CourseDescription = ({ course }) => {
  return (
    <div>
      <h1>{course.title}</h1>
      <p>
        <strong>Course Overview</strong>
      </p>
      {course.description.map((overview, i) => (
        <p key={i}>{overview}</p>
      ))}
      <br />

      <p>
        <strong>Who Should Attend</strong>
      </p>
      <p>{course.targetAudience}</p>

      <p>
        <strong>Material Requirements</strong>
      </p>
      <p>{course.prerequisites}</p>

      <hr />

      <p>
        <strong>Agenda</strong>
      </p>

      <div className="row">
        {course.agenda.map((agenda, i) => {
          const name =
            agenda.day === 1
              ? "Day One"
              : agenda.day === 2
              ? "Day Two"
              : "Day Three";
          return (
            <div className="col-sm-6" key={i}>
              <table>
                <tr>
                  <th>{name}</th>
                </tr>
                <tr>
                  <td>
                    <ul>
                      {agenda.value.map((val, i) => (
                        <li key={i}>{val}</li>
                      ))}
                    </ul>
                  </td>
                </tr>
              </table>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const CourseDetailPage = () => {
  const [course, setCourse] = useState({});
  const [classes, setClasses] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();
  const list = ["Home", "Courses", course.courseNum];

  useEffect(() => {
    sendRequest({ url: `/courses/${params.id}` }, setCourse).catch((_) => {});
    sendRequest({ url: `/course/classes/${params.id}/` }, setClasses).catch(
      (_) => {}
    );
  }, [params.id, sendRequest]);

  return (
    <>
      <BreadCrumbs list={list} title="Courses" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      {course.id !== undefined && (
        <div className="container p-4">
          <div className="row">
            <div className="col-sm-8">
              {course.title && <CourseDescription course={course} />}
            </div>
            <div className="col-sm-4 h-100">
              <h3>Upcoming Classes</h3>
              <a className="btn btn-dark text-white w-100" href="/classes">
                View Training Schedule
              </a>
              <div
                style={{ overflowX: "hidden", overflowY: "auto" }}
                className="h-100"
              >
                {classes.length > 0 ? (
                  classes.map((cls) => {
                    return (
                      <>
                        <div>
                          <p className="p-0 m-0">{cls.hostname}</p>
                          <p className="p-0 m-0">{cls.location}</p>
                          <p className="p-0 m-0">
                            {giveProperDate(cls.startDate)}
                          </p>
                          <p className="p-0 m-0">{cls.instructor}</p>
                          <a
                            href={`/classes/register/${cls.id}`}
                            className="text-primary border-0  "
                          >
                            Register Now
                          </a>
                        </div>
                        <hr />
                      </>
                    );
                  })
                ) : (
                  <p>
                    There are currently no scheduled classes for this course.
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default CourseDetailPage;
