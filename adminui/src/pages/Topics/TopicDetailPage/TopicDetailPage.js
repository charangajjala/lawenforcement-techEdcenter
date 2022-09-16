import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import useHttp from "../../../hooks/use-http";
import useInput from "../../../hooks/use-input";
import useAlert from "../../../hooks/use-alert";
import Col from "../../../util/components/Col";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import SetAlert from "../../../util/components/SetAlert";

const TopicDetailPage = ({ mode, isModal, modalFunc }) => {
  console.log("-----TopicDetailPage--------");
  const [topic, setTopic] = useState({ createdBy: {} });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const list =
    mode === "EDIT"
      ? [
          { name: "Home", path: "/home" },
          { name: "Topics", path: "/courses/topics" },
          { name: `${topic.name} ` },
        ]
      : [
          { name: "Home", path: "/home" },
          { name: "Topics", path: "/courses/topics" },
          "",
        ];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    if (mode === "EDIT") {
      sendRequest({ url: `courses/topics/${params.id}` }, setTopic);
    }
  }, [mode, sendRequest, params.id]);

  const [topicName, topicNameHandler] = useInput(
    mode === "EDIT" ? topic.name : null
  );

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Topic `)) {
      try {
        await fileRequest(
          { method: "DELETE", url: `/topics/${topic.id}` },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {
        if (error !== "refresh success") {
        }
      }
    }
  };

  const submitHandler = async (e) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const newTopic = { name: topicName };
    if (mode === "EDIT" && newTopic.name === topic.name) {
      delete newTopic["name"];
    }

    console.log("new", newTopic);
    try {
      if (Object.keys(newTopic).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            { method: "POST", url: "/courses/topics/", body: newTopic },
            modalFunc
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/courses/topics/${params.id}`,
              body: newTopic,
            },
            null
          );
        console.log("<<<<sent req in submit>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (e) {}
  };

  return (
    <div className="container-fluid p-5">
      {!isModal && <BreadCrumbs list={list} mode={true} />}
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form className="cd" onSubmit={submitHandler}>
        <div className="row 1">
          <Col
            col="col-md-4 "
            label="Topic Name"
            value={topicName}
            onChange={topicNameHandler}
            required={true}
          />
          {mode === "EDIT" && (
            <div className="col-md-4">
              <h5>Created</h5>
              <h6>{topic.created}</h6>
            </div>
          )}
          {mode === "EDIT" && (
            <div className="col-md-4">
              <h5>Created By</h5>
              <h6>
                {`${topic.createdBy.firstName} ${topic.createdBy.lastName}`}
              </h6>
            </div>
          )}
        </div>
        <button type="submit" className="btn btn-primary">
          Save
        </button>
        {mode === "EDIT" && (
          <button className="btn btn-danger mx-5" type="button" onClick={del}>
            Delete Topic
          </button>
        )}
      </form>
    </div>
  );
};

export default TopicDetailPage;
