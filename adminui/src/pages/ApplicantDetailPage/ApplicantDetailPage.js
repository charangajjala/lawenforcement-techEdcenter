import React, {
  useEffect,
  useState,
  useRef,
  useCallback,
  useMemo,
} from "react";
import { useParams } from "react-router-dom";
import useInput from "../../hooks/use-input";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import Col from "../../util/components/Col";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import SetAlert from "../../util/components/SetAlert";
import SelectEntity from "../../util/components/SelectEntity";
import {
  adjust,
  getData,
  checkIfEdited,
  checkAddEmpty,
} from "../../util/helper-functions/util-functions";
import FileUpload from "../../util/components/FileUpload";
import SelectOne from "../../util/components/SelectOne";
import { selectStatus } from "../../constants/selectConstants";
import Notes from "../../util/components/Notes";

const ApplicantDetailPage = ({ mode }) => {
  const [applicant, setApplicant] = useState({ createdBy: {} });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectCourses, setSelectCourses] = useState([]);
  const [selectUsers, setSelectUsers] = useState([]);

  const list =
    mode === "EDIT"
      ? [
          { name: "Home", path: "/home" },
          { name: "applicants", path: "/instructors/applicants" },
          { name: `${applicant.id} ` },
        ]
      : [
          { name: "Home", path: "/home" },
          { name: "applicants", path: "/instructors/applicants" },
          "",
        ];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest(
            { url: `instructors/applicants/${params.id}` },
            setApplicant,
            true
          );
        }
        await sendRequest({ url: "/courses/" }, setSelectCourses,true);
        await sendRequest({ url: "/users/" }, setSelectUsers);
      } catch (error) {
        //handle error
      }
    };
    fetch();
  }, [mode, params.id, sendRequest]);

  const selectTransformUsers = useMemo(
    () =>
      selectUsers.map((user) => {
        return { id: user.id, username: `${user.firstName} ${user.lastName}` };
      }),
    [selectUsers]
  );

  const [comments, commentsHandler] = useInput(applicant.comments);

  const courses = useRef([]);
  const docs = useRef([]);
  const adminNotes = useRef([]);
  const userid = useRef();
  const status = useRef("");

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Applicant  `)) {
      try {
        await sendRequest(
          {
            method: "DELETE",
            url: `/instructors/applicants/${applicant.id}`,
          },
          null,
          
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {
       
      }
    }
  };

  const submitHandler = async (e, ) => {
    if (e) e.preventDefault();
    try {
      const setDocId = (doc, id) => {
        doc.id = id.id;
      };

      for (const doc of docs.current) {
        if (doc.old !== true && doc.action === "ADD" && doc) {
          await fileRequest(
            { url: "/file/", method: "POST", body: doc.file },
            setDocId.bind(null, doc),
            doc.name,
            
          );
        }
      }
      const newApplicant = {
        userId: parseInt(userid.current),
        courses: adjust(courses.current,mode),
        docs: adjust(docs.current,mode),
        comments,
        status: status.current,
        adminNotes: adminNotes.current,
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
              url: `/instructors/applicants/${params.id}`,
              body: newApplicant,
            },
            null,
            
          );
        console.log("<<<<sent req in submit>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {
     
    }
  };

  const col = "col";
  const cb = useCallback(getData, []);

  return (
    <div className="container-fluid p-5">
      <BreadCrumbs list={list} mode={true} />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
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
            reuired={true}
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
          <Notes notes={applicant.adminNotes} cb={cb} cbref={adminNotes} />
          <SelectOne
            cb={cb}
            cbref={status}
            selectEntitys={selectStatus}
            data={applicant.status}
            show="status"
            comp="status"
            val="status"
            title="Status"
            initTxt="Select Status"
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
  );
};

export default ApplicantDetailPage;
