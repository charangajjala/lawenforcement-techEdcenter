import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import useHttp from "../hooks/use-http";
import BreadCrumbs from "../util/components/BreadCrumbs";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";
import { CourseDescription } from "./CourseDetailPage";
import { InstructorDescription } from "./InstructorsPage";
import fileDownload from "js-file-download";

const ClassDetailPage = () => {
  const [cls, setClass] = useState({ host: {}, location: { address: {} } });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const [course, setCourse] = useState({});
  const [instructor, setInstructor] = useState({});

  const params = useParams();
  const list = ["Home", "Classes", "Register"];

  useEffect(() => {
    sendRequest({ url: `/classes/${params.id}` }, setClass).catch(() => {});
  }, [params.id, sendRequest]);

  useEffect(() => {
    async function fetch() {
      try {
        await sendRequest(
          { url: `/instructors/${cls.instructor}` },
          setInstructor
        );
        await sendRequest({ url: `/courses/${cls.course}` }, setCourse);
      } catch (error) {}
    }
    if (cls.id) fetch();
  }, [params.id, sendRequest, cls]);

  const downloadFlyer = async (e) => {
    try {
      await sendRequest(
        {
          url: `flyer/download/${cls.id}/`,
          method: "POST",
          responseType: "blob",
        },
        (res) => {
          fileDownload(res, "flyer.pdf");
        }
      );
    } catch (error) {}
  };

  return (
    <>
      <BreadCrumbs list={list} title="Register" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <div className="container">
        <div className="row">
          <h1>{course.title}</h1>
        </div>
        <br />

        <div className="row">
          <div className="col-sm-6">
            <table className="table table-sm">
              <tbody>
                <tr>
                  <td>
                    <strong>Host :</strong>
                  </td>
                  <td>{cls.host.name}</td>
                </tr>
                <tr>
                  <td>
                    <strong>Location :</strong>
                  </td>
                  <td>
                    {cls.location.address
                      ? `${cls.location.address.address1}, ${cls.location.address.city}, ${cls.location.address.state}, ${cls.location.address.zip}`
                      : cls.location}
                  </td>
                </tr>
                <tr>
                  <td>
                    <strong>Dates :</strong>
                  </td>
                  <td>
                    {cls.startDate} to {cls.endDate}
                  </td>
                </tr>
                <tr>
                  <td>
                    <strong>Times :</strong>
                  </td>
                  <td>
                    {cls.startTime} - {cls.endTime}
                  </td>
                </tr>
                <tr>
                  <td>
                    <strong>Fee :</strong>
                  </td>
                  <td>
                    <span
                      className={`${
                        cls.earlyFee === cls.fee
                          ? "btn-success"
                          : "btn-outline-success"
                      }  btn-sm mx-1  btn `}
                    >{`Early: $${cls.earlyFee}`}</span>
                    <span
                      className={`${
                        cls.regularFee === cls.fee
                          ? "btn-success"
                          : "btn-outline-success"
                      }   btn-sm mx-1 btn `}
                    >{`Regular: $${cls.regularFee}`}</span>
                    <span
                      className={`${
                        cls.lateFee === cls.fee
                          ? "btn-success"
                          : "btn-outline-success"
                      }   btn-sm mx-1  btn`}
                    >{`Late: $${cls.lateFee}`}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="col-sm-4">
            <img src={cls.host.logo} className="img-fluid" alt="logo" />
          </div>
          <div className="col-sm-2">
            <table id="class-flyer-register">
              <tr>
                <td>
                  <button
                    className="btn btn-outline-primary"
                    onClick={downloadFlyer}
                  >
                    Class Flyer
                  </button>
                </td>
              </tr>
              <tr>
                <td>
                  <a
                    href={`/classes/register/${cls.id}`}
                    className="btn btn-outline-primary"
                  >
                    Register
                  </a>
                </td>
              </tr>
            </table>
          </div>
        </div>
        <br />

        <div className="row">
          <ul className="nav nav-pills  bg-white" role="tablist">
            <li className="nav-item">
              <a
                className="nav-link active"
                data-toggle="pill"
                href="#course-description"
              >
                Course Description
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link"
                data-toggle="pill"
                href="#about-instructor"
              >
                About Instructor
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" data-toggle="pill" href="#travel-info">
                Travel Information
              </a>
            </li>
          </ul>
          <hr />

          <div className="tab-content">
            <div id="course-description" className="tab-pane active">
              <br />
              {course.title && <CourseDescription course={course} />}
            </div>
            <div id="about-instructor" className="tab-pane fade">
              <br />
              {instructor.firstName && (
                <InstructorDescription instructor={instructor} />
              )}
            </div>
            <div id="travel-info" className="tab-pane fade">
              <br />
              <table className="table table-sm table-borderless">
                <tr>
                  <th>Host:</th>
                  <td>{cls.host.name}</td>
                </tr>
                <tr>
                  <th>Location:</th>
                  <td>
                    {cls.location.address
                      ? `${cls.location.address.address1}, ${cls.location.address.city}, ${cls.location.address.state}, ${cls.location.address.zip}`
                      : cls.location}
                  </td>
                </tr>
                <tr>
                  <th>Recommended Hotels:</th>
                  <td> No hotels found.</td>
                </tr>
              </table>
            </div>
          </div>
        </div>
      </div>

      <br />
      <div className="row"></div>
    </>
  );
};

export default ClassDetailPage;
