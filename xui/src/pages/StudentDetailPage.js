import React, {
  useState,
  useEffect,
  useRef,
  useCallback,
  useMemo,
} from "react";
import useInput from "../hooks/use-input";
import useHttp from "../hooks/use-http";
import { useParams } from "react-router-dom";
import Col from "../util/components/Col";

import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";
import {
  adjust,
  getData,
  checkIfEdited,
  checkAddEmpty,
} from "../util/helper-functions/util-functions";
import FileUpload from "../util/components/FileUpload";
import SelectOne from "../util/components/SelectOne";

const StudentDetailPage = ({ mode }) => {
  const [student, setStudent] = useState({});
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectUsers, setSelectUsers] = useState([]);
  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest({ url: `/students/` }, setStudent);
        }
        await sendRequest({ url: "/users/team/" }, setSelectUsers);
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
  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [agency, agencyHandler] = useInput(useInputInit(student.agencyName));
  const [comments, commentsHandler] = useInput(useInputInit(student.comments));
  const docs = useRef([]);
  const userid = useRef("");

  const cb = useCallback(getData, []);
  const col = "col-md-4";

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Student `)) {
      try {
        await sendRequest({ method: "DELETE", url: `/students/` }, null);
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
        if (doc.old !== true && doc.action === "ADD") {
          await fileRequest(
            { url: "/file/", method: "POST", body: doc.file },
            setDocId.bind(null, doc),
            doc.name
          );
        }
      }
      const newStudent = {
        userId: userid.current,
        docs: adjust(docs.current),
        comments,
        agencyName: agency,
      };
      console.log("old", newStudent);
      checkAddEmpty(newStudent);
      if (mode === "EDIT") {
        checkIfEdited(newStudent, student);
      }
      console.log("new ", newStudent);
      if (Object.keys(newStudent).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            {
              method: "POST",
              url: "/students/",
              body: newStudent,
            },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/students/`,
              body: newStudent,
            },
            null
          );
        console.log("<<<<<sent req in submit>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };
  return (
    <>
      <div>
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <div className="container">
          <form className="cd " onSubmit={submitHandler}>
            <div className="row">
              {" "}
              <Col
                col={"col-md-4"}
                label="Agency"
                value={agency}
                onChange={agencyHandler}
                required={true}
              />
              <Col
                col="col-md"
                label="Comments"
                value={comments}
                onChange={commentsHandler}
                type="textarea"
              />
            </div>
            <div className="row">
              <SelectOne
                col="col-md-4"
                cb={cb}
                cbref={userid}
                data={student.userId}
                selectEntitys={selectTransformUsers}
                comp="id"
                show="username"
                val="id"
                title="User"
                required={true}
                initTxt="Select User"
              />
              <FileUpload
                cb={cb}
                cbref={docs}
                mode={mode}
                data={student.docs}
                title="Docs"
              />
            </div>

            <button type="submit" className="btn btn-primary">
              Save
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export default StudentDetailPage;
