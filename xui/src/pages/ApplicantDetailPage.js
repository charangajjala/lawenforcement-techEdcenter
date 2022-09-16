import React, {
  useEffect,
  useState,
  useRef,
  useCallback,
  useMemo,
} from "react";
import { useParams } from "react-router-dom";
import useInput from "../hooks/use-input";
import useAlert from "../hooks/use-alert";
import useHttp from "../hooks/use-http";
import Col from "../util/components/Col";
import BreadCrumbs from "../util/components/BreadCrumbs";
import SetAlert from "../util/components/SetAlert";
import SelectEntity from "../util/components/SelectEntity";
import {
  adjust,
  getData,
  checkIfEdited,
  checkAddEmpty,
} from "../util/helper-functions/util-functions";
import FileUpload from "../util/components/FileUpload";
import SelectOne from "../util/components/SelectOne";

const ApplicantDetailPage = ({ mode }) => {
  const [applicant, setApplicant] = useState({});
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectCourses, setSelectCourses] = useState([]);
  const [selectUsers, setSelectUsers] = useState([]);

  const list = ["Home", "Applicant"];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest({ url: `instructors/applicants/` }, setApplicant);
        }
        await sendRequest({ url: "/courses/" }, setSelectCourses);
        await sendRequest({ url: "/users/team/" }, setSelectUsers);
      } catch (error) {
        //handle error
      }
    };
    fetch();
  }, [mode, params.id, sendRequest]);

  console.log("check", selectCourses);
  console.log(selectUsers);

  const selectTransformUsers = useMemo(
    () =>
      selectUsers.map((user) => {
        return { id: user.id, username: `${user.firstName} ${user.lastName}` };
      }),
    [selectUsers]
  );

  console.log("checknew", selectUsers);

  const [comments, commentsHandler] = useInput(applicant.comments);

  const courses = useRef([]);
  const docs = useRef([]);

  const userid = useRef();

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Applicant  `)) {
      try {
        await sendRequest(
          {
            method: "DELETE",
            url: `/instructors/applicants/`,
          },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {}
    }
  };

  const submitHandler = async (e) => {
    if (e) e.preventDefault();
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
      const newApplicant = {
        userId: parseInt(userid.current),
        courses: adjust(courses.current),
        docs: adjust(docs.current),
        comments,
      };
      console.log("old", newApplicant);
      checkAddEmpty(newApplicant);
      if (mode === "EDIT") {
        checkIfEdited(newApplicant, applicant);
      }
      console.log("new", newApplicant);
      if (Object.keys(newApplicant).length !== 0) {
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/instructors/applicants/`,
              body: newApplicant,
            },
            null
          );
        if (mode === "ADD")
          await sendRequest(
            {
              method: "POST",
              url: `/instructors/applicants/`,
              body: newApplicant,
            },
            null
          );
        console.log("<<<<sent req in submit>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };

  const col = "col";
  const cb = useCallback(getData, []);

  return (
    <div>
      <BreadCrumbs list={list} title="Instructor Applicant" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <div className="container">
        <form className="cd" onSubmit={submitHandler}>
          <div className="row">
            <SelectEntity
              selectEntitys={selectCourses}
              named="title"
              data={applicant.courses}
              mode={mode}
              cb={cb}
              title="Select Courses"
              cbref={courses}
              required={true}
            />
            <FileUpload
              cb={cb}
              cbref={docs}
              data={applicant.docs}
              mode={mode}
              title="Docs"
            />
            <SelectOne
              cb={cb}
              cbref={userid}
              selectEntitys={selectTransformUsers}
              data={applicant.userId}
              show="username"
              comp="id"
              title="Users"
              val="id"
              required={true}
              initTxt="Select User"
            />
            <Col
              col={col}
              label="Comments"
              value={comments}
              onChange={commentsHandler}
              type="textarea"
              rows={6}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Save
          </button>
          {mode === "EDIT" && (
            <button className="btn btn-danger mx-5" type="button" onClick={del}>
              Delete Applicant
            </button>
          )}
        </form>
      </div>
    </div>
  );
};

export default ApplicantDetailPage;
