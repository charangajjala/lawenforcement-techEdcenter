import React, { useState, useEffect } from "react";
import ClsRow from "../../util/components/ClsRow";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import Modal from "../../util/components/Modal";
import DocPage from "./DocModalPage";
import { giveProperDate } from "../../util/helper-functions/util-functions";

const CurrentClass = ({ current, sendRequest }) => {
  const Traveljsx = () => {
    return (
      <div className="container">
        {current.tavelInfo && (
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

  const AAR = () => {
    const questions = ["q1", "q2"];
    return (
      <div className="container">
        {current.aar &&
          questions.map((q, i) => {
            return (
              <div key={i}>
                <h3>{q}</h3>
                Answer : {current.aar[i]}
              </div>
            );
          })}
      </div>
    );
  };

  const Evaluations = () => {
    const questions = ["q1", "q2"];

    const calAvg = (i) => {
      let sum = 0;
      for (const evaluation of current.evaluation) {
        sum += evaluation[`q${i}`];
      }
      return (sum / current.evaluation.length).toFixed(2);
    };

    const calPercent = (i) => {
      let trueCount = 0;
      for (const evaluation of current.evaluation) {
        if (evaluation[`q${i}`] === true) trueCount++;
      }
      return ((trueCount / current.evaluation.length) * 100).toFixed(2);
    };

    return (
      <div className="container">
        {current.evaluation && (
          <table className="table table-striped">
            <thead>
              <tr>
                <th scope="col">Question</th>
                <th scope="col">Avergae Rating</th>
              </tr>
            </thead>
            <tbody>
              {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => {
                return i < 9 ? (
                  <tr key={i}>
                    <td>{questions[i]}</td>
                    <td>{calAvg(i + 1)}</td>
                  </tr>
                ) : (
                  <tr key={i}>
                    <td>{questions[i]}</td>
                    <td>
                      {`True: ${calPercent(i + 1)}% False: ${
                        100 - calPercent(i + 1)
                      }%`}
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

  return (
    <div className="">
      <div className="row">
        <div className="col-sm-8">
          <div className="row">
            <div className="col-sm-8">
              <table className="table ">
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
                  <ClsRow name="Status" val={current.status} />
                </tbody>
              </table>
            </div>

            <div className="col-sm-4">
              <table className="table ">
                <tbody>
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
                        thisModal={`Travel${current.id}`}
                      />
                    }
                    thisModal="Travel Info"
                  />
                  <ClsRow
                    name="Class Materials"
                    val={
                      <Modal
                        Component={DocPage}
                        mdltitle="View/Edit"
                        props={{
                          url: `classes/instructor/docs/${current.id}`,
                          initdocs: current.docs,
                        }}
                        thisModal={`Class Materials ${current.id}`}
                      />
                    }
                  />
                  <ClsRow
                    name="Evaluations"
                    val={
                      <Modal
                        Component={Evaluations}
                        mdltitle="View"
                        thisModal={`Evaluations${current.id}`}
                      />
                    }
                  />
                  <ClsRow
                    name="AAR"
                    val={
                      <Modal
                        Component={AAR}
                        mdltitle="View"
                        thisModal={`AAR${current.id}`}
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

const InstructorPastClasses = () => {
  const [currents, setCurrents] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest({ url: "/classes/instructor/past/" }, setCurrents).catch(
      (_) => {}
    );
  }, [sendRequest]);

  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      {currents.map((current) => (
        <CurrentClass
          current={current}
          key={current.id}
          sendRequest={sendRequest}
        />
      ))}
    </div>
  );
};

export default InstructorPastClasses;
