import React, {
  useState,
  useEffect,
  useRef,
  useCallback,
  useMemo,
} from "react";
import useInput from "../../hooks/use-input";
import useHttp from "../../hooks/use-http";
import { useParams } from "react-router-dom";
import Col from "../../util/components/Col";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import {
  adjust,
  getData,
  checkIfEdited,
  checkAddEmpty,
} from "../../util/helper-functions/util-functions";
import FileUpload from "../../util/components/FileUpload";
import SelectOne from "../../util/components/SelectOne";
import Notes from "../../util/components/Notes";

const StudentDetailPage = ({ mode }) => {
  const [student, setStudent] = useState({
    createdBy: {},
  });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectUsers, setSelectUsers] = useState([]);

  const list =
    mode === "EDIT"
      ? ["Home", "Students", `${student.id}`]
      : ["Home", "Students", ""];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest({ url: `/students/${params.id}` }, setStudent);
        }
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
  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [agency, agencyHandler] = useInput(useInputInit(student.agencyName));
  const [comments, commentsHandler] = useInput(useInputInit(student.comments));

  const [active, activeHandler] = useInput(
    useInputInit(student.isActive),
    "checkbox"
  );

  const docs = useRef([]);
  const userid = useRef("");
  const adminNotes = useRef([]);
  const cb = useCallback(getData, []);

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Student `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/students/${student.id}` },
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
        docs: adjust(docs.current, mode),
        isActive: active,
        adminNotes: adminNotes.current,
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
              url: `/students/${params.id}`,
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

  const req = !!active;
  return (
    <>
      <div className="container-fluid p-5">
        <BreadCrumbs list={list} />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="cd " onSubmit={submitHandler}>
          <div className="row">
            {" "}
            <Col
              col={"col-md"}
              label="Agency"
              value={agency}
              onChange={agencyHandler}
              required={req}
            />
            <Col
              col="col-md"
              label="Comments"
              value={comments}
              onChange={commentsHandler}
              type="textarea"
            />
            <Col
              col={"col-md"}
              label="Active"
              value={active}
              onChange={activeHandler}
              type="checkbox"
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

            <Notes cb={cb} cbref={adminNotes} notes={student.adminNotes} />
          </div>
          <div className="row">
            {mode === "EDIT" &&
              !!student.createdBy &&
              !!student.createdBy.firstName && (
                <div className="row 6">
                  <div className="col-md-4">
                    <h5>Created</h5>
                    <h6>{student.created}</h6>
                  </div>
                  <div className="col-md-4">
                    <h5>Created By</h5>
                    <h6>
                      {`${student.createdBy.firstName} ${student.createdBy.lastName}`}
                    </h6>
                  </div>
                </div>
              )}
          </div>

          <button type="submit" className="btn btn-primary">
            Save
          </button>
          {mode === "EDIT" && (
            <button className="btn btn-danger mx-5" type="button" onClick={del}>
              Delete Host
            </button>
          )}
        </form>
      </div>
    </>
  );
};

export default StudentDetailPage;
