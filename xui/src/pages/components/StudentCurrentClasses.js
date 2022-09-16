import React, { useState, useEffect, useRef } from "react";
import ClsRow from "../../util/components/ClsRow";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import Modal from "../../util/components/Modal";
import { Link } from "react-router-dom";
import {giveProperDate} from "../../util/helper-functions/util-functions";

const Attendance = ({ current, setClose }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const acode = useRef("");
  const submit = async (e) => {
    try {
      e.preventDefault();
      await sendRequest({
        url: `/classes/student/attendance/${current.id}/`,
        method: "POST",
        params: { attendanceCode: acode.current.value },
      });
      setShowAlert(true);
      setAlertMessage("Posted the Attendance Successfully");
      setClose(true);
    } catch (error) {}
  };

  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={submit}>
        Access Code:{" "}
        <input type="text" placeholder="Access Code" required ref={acode} />
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
};

const CurrentClass = ({ currentt, sendRequest }) => {
  const [current, setCurrent] = useState({});
  useEffect(() => {
    setCurrent(currentt);
  }, [currentt]);

  const [close, setClose] = useState(false);

  const canGiveAttendance =
    new Date(current.startDate).getTime() <=
    new Date().getTime() <=
    new Date(current.endDate).getTime();

  return (
    <div>
      <div className="row">
        <div className="col-sm-8">
          <div className="row">
            <div className="col-sm-6">
              <table className="table table-bordered">
                <tbody>
                  {" "}
                  <ClsRow name="Course" val={current.course} />
                  <ClsRow
                    name="Dates"
                    val={giveProperDate(current.startDate, current.endDate)}
                  />
                  <ClsRow
                    name="Times"
                    val={`${current.startTime} to ${current.endTime}`}
                  />
                </tbody>
              </table>
            </div>

            <div className="col-sm-6">
              <table className="table table-bordered">
                <tbody>
                  {" "}
                  <ClsRow name="Location" val={current.location} />
                  <ClsRow name="Host" val={current.host} />
                  <ClsRow name="Instructor" val={current.instructor} />
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="col-sm-4">
          <div className="row">
            <div className="col-sm-auto">
              Invoice No:{current.invoiceNum}
              <Link
                to={`/invoice/${current.invoiceNum}/${current.accessKey}`}
              >
                <button className="btn btn-primary btn-sm mx-1">
                  Check Invoice
                </button>
              </Link>
            </div>
            {canGiveAttendance && (
              <div className="col-sm-auto">
                {!current.attendance ? (
                  <Modal
                    mdltitle="Attendance"
                    Component={Attendance}
                    props={{ current, setClose }}
                    thisModal={`Attendance${current.id}`}
                    onClose={(_) => {
                      if (close) {
                        current.attendance = true;
                        setCurrent({ ...current });
                        setClose(false);
                      }
                    }}
                  />
                ) : (
                  <button className="btn btn-primary" disabled>
                    Attendance
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const StudentCurrentClasses = () => {
  console.log("<<Student Current Classes>>");
  const [currents, setCurrents] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest({ url: "/classes/student/current/" }, setCurrents).catch(
      (err) => {}
    );
  }, [sendRequest]);

  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      {currents.map((current) => (
        <CurrentClass
          currentt={current}
          sendRequest={sendRequest}
          key={current.id}
        />
      ))}
    </div>
  );
};

export default StudentCurrentClasses;
