import React, { useState, useEffect, useRef, useCallback } from "react";
import ClsRow from "../../util/components/ClsRow";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import Modal from "../../util/components/Modal";
import FileUpload from "../../util/components/FileUpload";
import { getData, adjust ,giveProperDate} from "../../util/helper-functions/util-functions";

const RosterTable = ({ toggle, students, signin, toggleAttendance }) => {
  return (
    <div className="container">
      {students && (
        <table class="table table-borderless table-striped table-sm">
          <tr class="border bg-primary text-white">
            <th>Student Id</th>
            <th>Title</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Agency</th>
            <th></th>
          </tr>
          <tbody>
            {students.map((student) => {
              const signedin = student.attendance;
              return (
                <tr key={student.studentId}>
                  <td>{student.studentId}</td>
                  <td>{student.title}</td>
                  <td>{student.firstName}</td>
                  <td>{student.lastName}</td>
                  <td>{student.agency}</td>
                  <td>
                    {toggle ? (
                      <div className="form-check">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          onChange={(e) => {
                            e.persist();
                            toggleAttendance(e, student.studentId);
                          }}
                          checked={signedin}
                        />
                        <label
                          className="form-check-label"
                          for="flexCheckDefault"
                        >
                          Sign In
                        </label>
                      </div>
                    ) : (
                      <button
                        className={`btn ${
                          signedin ? "btn-success" : "btn-primary"
                        }`}
                        disabled={!!signedin}
                        onClick={() => signin(student.studentId)}
                      >
                        {signedin ? "Signed In" : "Sign In"}
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
};

const Roster = ({ students, clsid }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const [studentss, setStudentss] = useState([]);

  useEffect(() => {
    if (students) {
      setStudentss(students);
    }
  }, [students]);

  const signin = (id) => {
    setStudentss((prev) => {
      prev.find((s) => s.studentId === id).attendance = true;
      return [...prev];
    });
  };

  const postAttendence = async (studentId) => {
    try {
      await sendRequest(
        {
          url: `/classes/instructor/attendance/${clsid}/`,
          method: "PUT",
          body: { studentId },
        },
        null
      );
      signin(studentId);
    } catch (error) {}
  };
  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <RosterTable
        students={studentss}
        signin={postAttendence}
        toggle={false}
      />
    </div>
  );
};

const CloseClass = ({ students, clsid, clsdocs }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] =
    useAlert(true); //refresh
  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const answers = useRef([]);
  const questions = ["q1", "q2"];
  const handler = (e, i) => {
    answers.current[i] = e.target.value;
  };
  const [studentss, setStudentss] = useState([]);

  useEffect(() => {
    if (students) {
      setStudentss(students);
    }
  }, [students]);

  const docs = useRef([]);
  const cb = useCallback(getData, []);

  const toggleAttendance = (e, id) => {
    setStudentss((prev) => {
      prev.find((s) => s.studentId === id).attendance = e.target.checked;
      return [...prev];
    });
  };

  const postAttendence = async (e) => {
    e.stopPropagation();
    e.preventDefault();
    try {
      const setDocId = (doc, id) => {
        doc.id = id.id;
      };

      for (const doc of docs.current) {
        if (doc && doc.old !== true && doc.action === "ADD") {
          await fileRequest(
            { url: "/file/", method: "POST", body: doc.file },
            setDocId.bind(null, doc),
            doc.name
          );
        }
      }

      const body = {
        aar: answers.current,
        attendance: studentss
          .filter((s) => s.attendance === true)
          .map((s) => s.studentId),
        docs: adjust(docs.current, "EDIT"),
      };
      if (docs.current.length === 0) delete body["docs"];
      await sendRequest(
        {
          url: `/classes/instructor/close/${clsid}`,
          method: "POST",
          body,
        },
        null
      );
      setShowAlert(true);
      setAlertMessage("Class is Closed Successfully");
    } catch (error) {}
  };
  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={postAttendence}>
        <RosterTable
          students={studentss}
          toggleAttendance={toggleAttendance}
          toggle={true}
        />
        <h3>AAR</h3>
        {questions.map((q, i) => (
          <div key={i}>
            {q}
            <div className="m-1">
              <input
                type="textarea"
                required
                onChange={(e) => {
                  handler(e, i);
                }}
              />
            </div>
          </div>
        ))}
        <FileUpload
          title="Class Materials"
          cbref={docs}
          cb={cb}
          col="col-12 m-1"
          data={clsdocs}
        />
        <button
          type="submit"
          className="btn btn-primary"
          onClick={postAttendence}
        >
          Close Class
        </button>
      </form>
    </div>
  );
};

const CurrentClass = ({ current, sendRequest }) => {
  const [acode, setACode] = useState("");

  const Traveljsx = () => {
    return (
      <div className="container">
        {current.travelInfo && (
          <div>
            {" "}
            Rent : {current.travelInfo.rentalInfo}
            <br />
            Flight : {current.travelInfo.flightInfo}
            <br />
            Hotel : {current.travelInfo.hotelInfo}
          </div>
        )}
      </div>
    );
  };

  const Attendancecodejsx = () => (
    <div>
      <h3>Attendance Code : {current.attendanceCode || acode} </h3>
    </div>
  );

  const openAttendance = async () => {
    const attendanceCode = Math.floor(1000 + (10000 - 1000) * Math.random());
    console.log("attendanceCode", attendanceCode);
    try {
      await sendRequest(
        {
          url: `classes/instructor/attendance/${current.id}/`,
          method: "POST",
          body: { attendanceCode },
        },
        null
      );
      setACode(attendanceCode);
    } catch (error) {}
  };

  const canCloseClass = () => {
    const present = new Date();
    const timearr = current.endTime.split(":");
    console.log(timearr);
    const enddate = new Date(current.endDate);
    enddate.setHours(parseInt(timearr[0]));
    enddate.setMinutes(parseInt(timearr[1]));
    console.log(present.getTime(), enddate.getTime());
    return present.getTime() >= enddate.getTime();
  };
  return (
    <div className="">
      <div className="row">
        <div className="col-sm-8">
          <div className="row">
            <div className="col-sm-8">
              <table className="table table-bordered">
                <tbody>
                  <ClsRow name="Course" val={current.course} />

                  <ClsRow
                    name="Dates"
                    val={giveProperDate(current.startDate,current.endDate)}
                  />

                  <ClsRow
                    name="Times"
                    val={`${current.startTime} to ${current.endTime}`}
                  />

                  <ClsRow name="Location" val={current.location} />
                  <ClsRow name="Host" val={current.host} />
                </tbody>
              </table>
            </div>

            <div className="col-sm-4">
              <table className="table table-bordered">
                <tbody>
                  <ClsRow name="Status" val={current.status} />
                  <ClsRow
                    name="Roster"
                    val={`${current.bookedSeats}/${current.totalSeats}`}
                  />
                  <ClsRow
                    name="Travel Info"
                    val={
                      <Modal
                        Component={Traveljsx}
                        mdltitle="View"
                        thisModal={`View ${current.id}`}
                      />
                    }
                  />
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="col-sm-auto">
          <div className="row">
            <div className="col-sm-auto">
              {!acode && !current.attendanceCode && (
                <button
                  type="button"
                  className="btn btn-primary btn-sm"
                  onClick={openAttendance}
                >
                  Open Attendance
                </button>
              )}
              {(!!acode || !!current.attendanceCode) && (
                <Modal
                  mdltitle="View Attendance Code"
                  Component={Attendancecodejsx}
                  thisModal={`Attendancecodejsx${current.id}`}
                />
              )}
            </div>
            <div className="col-sm-auto">
              <Modal
                mdltitle="Attendance"
                Component={Roster}
                props={{ students: current.roster, clsid: current.id }}
                thisModal={`Attedance${current.id}`}
              />
            </div>
            {canCloseClass() && (
              <div className="col-sm-auto">
                <Modal
                  mdltitle="Close Class"
                  Component={CloseClass}
                  props={{
                    students: current.roster,
                    clsid: current.id,
                    clsdocs: current.docs,
                  }}
                  thisModal={`Close Class ${current.id}`}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const InstructorCurrentClasses = () => {
  const [currents, setCurrents] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest({ url: "/classes/instructor/current/" }, setCurrents).catch(
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

export default InstructorCurrentClasses;
