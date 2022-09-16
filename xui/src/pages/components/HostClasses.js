import React, { useState, useEffect } from "react";
import ClsRow from "../../util/components/ClsRow";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import { Link } from "react-router-dom";
import { giveProperDate } from "../../util/helper-functions/util-functions";

const CurrentClass = ({ current, sendRequest }) => {
  return (
    <div>
      <div className="row">
        <div className="col-sm-8">
          <div className="row">
            <div className="col-sm-6">
              <table className="table table-bordered ">
                <tbody>
                  {" "}
                  <ClsRow name="Course" val={current.course} />
                  <ClsRow name="Instructor" val={current.instructor} />
                  <ClsRow
                    name="Dates"
                    val={giveProperDate(current.startDate,current.endDate)}
                  />
                </tbody>
              </table>
            </div>

            <div className="col-sm-6">
              <table className="table table-bordered">
                <tbody>
                  <ClsRow name="Location" val={current.location} />
                  <ClsRow name="Type" val={current.type} />
                  <ClsRow name="Status" val={current.status} />
                  <ClsRow
                    name="In Service Seats"
                    val={current.inServiceSeats}
                  />
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
                <button className="btn btn-primary m-1">Check Invoice</button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const HostCurrentClasses = ({ iscurrent }) => {
  console.log("<<Host Current Classes>>");
  const [currents, setCurrents] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest(
      { url: `/classes/host/${iscurrent ? "current/" : "past/"}` },
      setCurrents
    ).catch((err) => {});
  }, [sendRequest, iscurrent]);

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

export default HostCurrentClasses;
