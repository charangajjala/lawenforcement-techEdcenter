import React, { useState, useEffect, useRef, useCallback } from "react";
import useInput from "../../../hooks/use-input";
import useHttp from "../../../hooks/use-http";
import { useParams } from "react-router-dom";
import Agenda from "../../../util/components/Agenda";
import Desc from "../../../util/components/Desc";
import Col from "../../../util/components/Col";
import SelectEntity from "../../../util/components/SelectEntity";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import SetAlert from "../../../util/components/SetAlert";
import useAlert from "../../../hooks/use-alert";
import {
  giveTransformDesc,
  adjust,
  comapareArrays,
  getData,
  checkIfEdited,
  checkAddEmpty,
} from "../../../util/helper-functions/util-functions";
import "./CourseDetailPage.css";
import FileUpload from "../../../util/components/FileUpload";
import TopicDetailPage from "../../Topics/TopicDetailPage/TopicDetailPage";
import Modal from "../../../util/components/Modal";

const CourseDetailPage = ({ mode }) => {
  console.log("----CourseDetailPage----");
  const [course, setCourse] = useState({ createdBy: {} });
  const [selectTopics, setSelectTopics] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const modalFunc = useCallback((data) => {
    setSelectTopics((prev) => {
      prev.push(data);
      return [...prev];
    });
  }, []);

  const list =
    mode === "EDIT"
      ? ["Home", "Courses", `${course.courseNum}`]
      : ["Home", "Courses", ""];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();
  const setCourseData = (courseData) => {
    //do ...
    //sort agenda if not
    courseData.agenda.sort((a, b) => {
      return a.day - b.day;
    });
    setCourse(courseData);
  };

  useEffect(() => {
    async function fetch() {
      try {
        if (mode === "EDIT")
          await sendRequest({ url: `/courses/${params.id}` }, setCourseData);
        await sendRequest({ url: "/courses/topics/" }, setSelectTopics);
      } catch (error) {
        //handle error
      }
    }
    fetch();
  }, [sendRequest, params.id, mode]);

  const [title, titleHandler] = useInput(mode === "EDIT" ? course.title : null);
  const [isActive, activeHandler] = useInput(
    mode === "EDIT" ? course.isActive : null,
    "checkbox"
  );
  const [isNew, newHandler] = useInput(
    mode === "EDIT" ? course.isNew : null,
    "checkbox"
  );
  const [shortDesc, sdescHandler] = useInput(
    mode === "EDIT" ? course.shortDesc : null
  );
  const [subTitle, stitleHandler] = useInput(
    mode === "EDIT" ? course.subTitle : null
  );
  const [days, daysHandler] = useInput(String(course.days), "number");

  const [courseNum, courseNumHandler] = useInput(
    mode === "EDIT" ? course.courseNum : null
  );

  const [prerequisites, prereqHandler] = useInput(
    mode === "EDIT" ? course.prerequisites : null
  );

  const [targetAudience, targetAudienceHandler] = useInput(
    mode === "EDIT" ? course.targetAudience : null
  );

  const descObj = useRef({});
  const topics = useRef([]);
  const materials = useRef([]);

  const [agenda, setAgenda] = useState(
    mode === "ADD" ? [{ day: 1, value: [] }] : []
  );

  const agendas = useRef([]);
  const takeDataFromAgenda = useCallback(
    (agendaObj) => {
      if (agendas.current.length === 0) {
        agendas.current.push(agendaObj);
        return;
      }
      const existing = agendas.current.find(
        (agenda) => agenda.day === agendaObj.day
      );
      if (!existing) {
        agendas.current.push(agendaObj);
      }
      if (existing) existing.value = agendaObj.value;
    },
    [agendas]
  );

  const agendaAdd = () => {
    agenda.push({ day: agenda.length + 1, value: [] });
    setAgenda([...agenda]);
  };
  useEffect(() => {
    if (mode === "EDIT" && course.id) {
      setAgenda([...course.agenda]);
    }
  }, [course.id, mode, course.agenda]);

  const del = async () => {
    const delCourseNum = course.courseNum;
    if (window.confirm(`Is it okay to delete course ${delCourseNum}`)) {
      try {
        await sendRequest(
          {
            method: "DELETE",
            url: `/courses/${course.id}`,
          },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {}
    }
  };

  const submitHandler = async (e) => {
    try {
      if (e) e.preventDefault();

      const setMaterialId = (material, id) => {
        material.id = id.id;
      };

      for (const material of materials.current) {
        if (material.old !== true && material.action === "ADD") {
          await fileRequest(
            {
              url: "/file/",
              method: "POST",
              body: material.file,
              headers: { "content-type": "multipart/form-data" },
            },
            setMaterialId.bind(null, material),
            material.name
          );
        }
      }

      const newCourse = {
        courseNum,
        title,
        subTitle,
        shortDesc,
        description: giveTransformDesc(descObj.current),
        targetAudience,
        prerequisites,
        isActive,
        isNew,
        days: parseInt(days),
        topic: adjust(topics.current, mode),
        material: adjust(materials.current, mode),
        agenda: agendas.current
          .map((agenda) => {
            return { day: agenda.day, value: giveTransformDesc(agenda.value) };
          })
          .filter((agenda) => agenda.value.length !== 0),
      };
      console.log("old", newCourse);

      if (mode === "ADD") {
        checkAddEmpty(newCourse);
      }
      if (mode === "EDIT") {
        delete newCourse["agenda"];
        checkIfEdited(newCourse, course);

        newCourse.agenda = agendas.current
          .map((agenda) => {
            return { day: agenda.day, value: giveTransformDesc(agenda.value) };
          })
          .filter((agenda) => agenda.value.length !== 0);

        if (newCourse.agenda.length === 0) delete newCourse["agenda"];
        else if (newCourse.agenda.length === course.agenda.length) {
          let agendaSame = true;

          for (let i = 0; i < newCourse.agenda.length; i++) {
            if (
              !comapareArrays(newCourse.agenda[i].value, course.agenda[i].value)
            ) {
              agendaSame = false;
              break;
            }
          }
          if (agendaSame) delete newCourse["agenda"];
        }
      }
      console.log("new", newCourse);

      if (Object.keys(newCourse).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            {
              method: "POST",
              url: "/courses/",
              body: newCourse,
            },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/courses/${params.id}`,
              body: newCourse,
            },
            null
          );
        console.log("<<<<<sent req in submit>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (e) {
      //handle error
    }
  };
  const cb = useCallback(getData, []);
  const col = "col-md";

  const required = !!isActive;
  return (
    <div className="container-fluid p-5">
      <BreadCrumbs list={list} />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form className="cd" onSubmit={submitHandler}>
        <div className="row 1">
          <Col
            col={col}
            label="Course Id"
            value={courseNum}
            onChange={courseNumHandler}
            required={true}
          />
          <Col
            col={col}
            label="Days"
            type="number"
            value={days}
            onChange={daysHandler}
            required={required}
          />
          <Col
            col={col}
            label="Title"
            value={title}
            onChange={titleHandler}
            required={required}
          />
        </div>
        <div className="row">
          <Col
            col={col}
            label="New"
            value={isNew}
            onChange={newHandler}
            type="checkbox"
          />
          <Col
            col={col}
            label="ACTIVE"
            value={isActive}
            onChange={activeHandler}
            type="checkbox"
          />

          <Col
            col={col}
            label="SubTitle"
            value={subTitle}
            onChange={stitleHandler}
            required={required}
          />
        </div>
        <div className="row 2">
          <Col
            col={col}
            label="Short Description"
            value={shortDesc}
            onChange={sdescHandler}
            type="textarea"
            required={required}
          />
          <Col
            col={col}
            label="Who Can Attend"
            value={targetAudience}
            onChange={targetAudienceHandler}
            type="textarea"
            required={required}
          />
          <Col
            col={col}
            label="Material Requirements"
            value={prerequisites}
            onChange={prereqHandler}
            type="textarea"
            required={required}
          />
        </div>
        <div className="row 4 ">
          <Desc
            descData={mode === "EDIT" ? course.description : null}
            title="Overview"
            cb={cb}
            cbref={descObj}
            required={required}
          />
          <div className="col-md-4">
            <div className="row p-0 m-0">
              <SelectEntity
                col="col-12 p-0 m-0 "
                selectEntitys={selectTopics}
                
                named="name"
                data={course.topic}
                mode={mode}
                cb={cb}
                title="Training Categories"
                cbref={topics}
              />
              <Modal
                addBtnName="Create Training Category"
                Component={TopicDetailPage}
                modalFunc={modalFunc}
              />
            </div>
          </div>
          <FileUpload
            cb={cb}
            cbref={materials}
            data={course.material}
            mode={mode}
            title="Course Materials"
          />
        </div>
        <div className="row 5 m-0 p-0">
          <div className="text-center m-0 p-0">
            <h4 className="m-0 p-0">Agenda</h4>
          </div>

          {agenda.map((agenda, i, agend) => {
            return (
              <React.Fragment key={agenda.day}>
                <Agenda
                  dayNum={agenda.day}
                  value={agenda.value}
                  cb={takeDataFromAgenda}
                  required={i === 0}
                />
                {(i === agend.length - 1) & (i !== 2) ? (
                  <div className="col-md-4 d-flex justify-content-center align-content-center">
                    <button className="btn btn-dark" onClick={agendaAdd}>
                      Add Another Day
                    </button>
                  </div>
                ) : (
                  false
                )}
              </React.Fragment>
            );
          })}
        </div>
        {mode === "EDIT" && (
          <div className="row 6">
            <div className="col-md-4">
              <h5>Created</h5>
              <h6>{course.created}</h6>
            </div>
            <div className="col-md-4">
              <h5>Created By</h5>
              <h6>
                {`${course.createdBy.firstName} ${course.createdBy.lastName}`}
              </h6>
            </div>
          </div>
        )}
        <input type="submit" value="Save" className="btn btn-primary" />
        {mode === "EDIT" && (
          <button className="btn btn-danger mx-4" type="button" onClick={del}>
            Delete Course
          </button>
        )}
      </form>
    </div>
  );
};

export default CourseDetailPage;
