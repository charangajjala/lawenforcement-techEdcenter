import React, { useState, useEffect, useRef, useCallback } from "react";
import { Link } from "react-router-dom";
import ClsRow from "../../util/components/ClsRow";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import Modal from "../../util/components/Modal";
import { giveProperDate } from "../../util/helper-functions/util-functions";

const Evaluations = ({ current, closeEvaluation, setClose }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const questions = ["q1", "q2"];
  const [rating, setRating] = useState({});
  const comments = useRef("");
  const interest = useRef("");

  const getRating = useCallback(
    (qi, rate) => {
      rating[`q${qi}`] = rate;
      setRating(rating);
    },
    [rating]
  );

  const radioChange = (e, i) => {
    rating[`r${i}`] = e.target.value;
    rating[`q${i}`] = e.target.value === "True" ? true : false;
    setRating({ ...rating });
  };

  const submit = async (e) => {
    e.preventDefault();
    rating.comments = comments.current.value;
    rating.interest = interest.current.value;
    if (rating.comments === "") delete rating["comments"];
    if (rating.interest === "") delete rating["interest"];
    for (const k in rating) {
      if (rating[k] === "True" || rating[k] === "False") delete rating[k];
    }
    try {
      await sendRequest({
        url: `/classes/student/evaluation/${current.id}`,
        method: "POST",
        body: rating,
      });
      closeEvaluation.current = closeEvaluation.current.bind(null, rating);
      setShowAlert(true);
      setAlertMessage("Posted the Evaluation Successfully");
      setClose(true);
    } catch (e) {}
  };

  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={submit}>
        {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => {
          return i < 9 ? (
            <div key={i}>
              <h3>{questions[i]}</h3>
              <Stars getRating={getRating.bind(null, i + 1)} />
            </div>
          ) : (
            <div key={i}>
              <h3>{questions[i]}</h3>
              <div>
                <input
                  type="radio"
                  value="True"
                  checked={rating[`r${i + 1}`] === "True"}
                  onChange={(e) => {
                    e.persist();
                    radioChange(e, i + 1);
                  }}
                  name={String(i)}
                  required
                />
                True
                <input
                  type="radio"
                  value="False"
                  checked={rating[`r${i + 1}`] === "False"}
                  onChange={(e) => {
                    e.persist();
                    radioChange(e, i + 1);
                  }}
                  name={String(i)}
                />{" "}
                False
              </div>
            </div>
          );
        })}
        <h3>Comments</h3>
        <textarea cols="50" rows="3" ref={comments}></textarea>
        <h3>Interest</h3>
        <textarea cols="50" rows="3" ref={interest}></textarea>
        <button type="submit" className="btn btn-primary  d-block ">
          Submit
        </button>
      </form>
    </div>
  );
};

const Stars = ({ getRating }) => {
  const [rating, setRating] = useState(0);

  useEffect(() => {
    getRating(rating);
  }, [rating, getRating]);

  return (
    <div>
      {[1, 2, 3, 4].map((i) => {
        return (
          <i
            className={`bi ${
              i > rating ? "bi-star" : "bi-star-fill text-warning "
            } `}
            key={i}
            onMouseEnter={() => setRating(i)}
            onMouseLeave={() => {
              if (i === 1) setRating(0);
            }}
          ></i>
        );
      })}
    </div>
  );
};

const CurrentClass = ({ currentt, sendRequest }) => {
  const [current, setCurrent] = useState(currentt);
  const [close, setClose] = useState(false);

  const closeEvaluation = useRef((evaluation) => {
    setCurrent((prev) => ({ ...prev, evaluation: evaluation }));
    setClose(false);
  });
  const ShowDocs = ({ docs }) => {
    return (
      <div className="container">
        {docs &&
          docs.map((doc, i) => {
            return (
              <div key={i}>
                {doc.name} Download: {doc.url}
              </div>
            );
          })}
      </div>
    );
  };

  const ShowEvaluations = () => {
    const questions = ["q1", "q2"];

    return (
      <div className="container">
        {current.evaluation && (
          <div>
            {questions.map((question, i) => {
              return (
                <div key={i}>
                  <h3>{question}</h3>
                  Answer: {current.evaluation[`q${i + 1}`]}
                </div>
              );
            })}
            <h3>Comments</h3>
            <p>{current.evaluation.comments}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div>
      <div className="row">
        <div className="col-sm-7">
          <div className="row">
            <div className="col-sm-6">
              <table className="table table-bordered ">
                <tbody>
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
                  <ClsRow name="Location" val={current.location} />
                  <ClsRow name="Host" val={current.host} />
                  <ClsRow name="Instructor" val={current.instructor} />
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="col-sm-4">
          <div className="row ">
            <div className="col-sm-4">
              <strong>Invoice No:</strong>
              {current.invoiceNum}
            </div>
            <div className="col-sm-4">
              <Link to={`/invoice/${current.invoiceNum}/${current.accessKey}`}>
                <button className="btn btn-primary btn-sm m-1">
                  Check Invoice
                </button>
              </Link>
            </div>
            <div className="col-sm-4">
              <Modal
                mdltitle="View Evaluation"
                Component={ShowEvaluations}
                thisModal={`Evaluations${current.id}`}
              />
            </div>
            <div className="col-sm-4"></div>
            <div className="col-sm-4">
              <Modal
                mdltitle="Course Materials"
                Component={ShowDocs}
                props={{ docs: current.courseMaterials }}
                thisModal={`Course Materials ${current.id}`}
              />
            </div>
            <div className="col-sm-4 ">
              <Modal
                mdltitle="Class Materials"
                Component={ShowDocs}
                props={{ docs: current.docs }}
                thisModal={`Class Materials ${current.id}`}
              />
            </div>
            <div className="col-sm-4"></div>
            {current.attendance && (
              <div className="col-sm-4 my-2">
                <Modal
                  mdltitle="Post Evaluation"
                  Component={Evaluations}
                  thisModal={`PostEvaluations${current.id}`}
                  props={{ current, closeEvaluation, setClose }}
                  onClose={(e) => {
                    if (close) {
                      closeEvaluation.current();
                    }
                  }}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const StudentPastClasses = () => {
  const [currents, setCurrents] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest({ url: "/classes/student/past/" }, setCurrents).catch(
      (err) => {}
    );
  }, [sendRequest]);

  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      {currents.map((current) => (
        <div>
          <CurrentClass
            currentt={current}
            sendRequest={sendRequest}
            key={current.id}
          />
          <hr />
        </div>
      ))}
    </div>
  );
};

export default StudentPastClasses;
