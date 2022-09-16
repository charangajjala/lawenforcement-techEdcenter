import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import BreadCrumbs from "../util/components/BreadCrumbs";
import useHttp from "../hooks/use-http";
import FilterInput from "../util/components/FilterInput";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";

const CoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [tracks, setTracks] = useState([]);
  const [topics, setTopics] = useState([]);
  const list = ["Home", "Courses"];
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    async function fetch() {
      try {
        await sendRequest({ url: "/courses/" }, setCourses);
        await sendRequest({ url: "/courses/tracks/" }, setTracks);
        await sendRequest({ url: "/courses/topics/" }, setTopics);
      } catch (error) {}
    }
    fetch();
  }, [sendRequest]);

  const filtcol = "col-sm-2 form-group";
  const strackid = useRef({ value: "" });
  const stopicid = useRef({ value: "" });
  const scid = useRef({ value: "" });
  const stitle = useRef({ value: "" });

  const resetFilters = (e) => {
    
    strackid.current.value = "";
    stopicid.current.value = "";
    scid.current.value = "";
    stitle.current.value = "";
    formref.current.reset();
  }


  const formref = useRef();


  const searchHandler = (e) => {
    if (e) e.preventDefault();

    const params = {
      scid: scid.current.value,
      stitle: stitle.current.value,
      stopicid: stopicid.current.value,
      strackid: strackid.current.value,
    };

    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/courses/", params: params }, setCourses);
    } catch (error) {
      //
    }
  };

  return (
    <>
      <BreadCrumbs list={list} title="Courses" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />

      <div className="container">
        <form className="row form-inline rounded my-4" onSubmit={searchHandler} ref={formref}>
          <FilterInput label="Course Id" col={filtcol} filtref={scid} />
          <FilterInput label="Title" col={filtcol} filtref={stitle} />
          <FilterInput
            label="Topics"
            options={topics}
            col={filtcol}
            show="name"
            val="id"
            filtref={stopicid}
          />
          <FilterInput
            label="Certification Tracks"
            options={tracks}
            col={filtcol}
            show="title"
            val="id"
            filtref={strackid}
          />
          <div className="col-sm-2 form-group">
            <input
              type="submit"
              className="btn btn-primary"
              name="search"
              value="Search"
            />
            <button
              type="button"
              className="btn btn-primary mx-3"
              onClick={resetFilters}
            >
              Reset
            </button>
          </div>
        </form>
        {courses.map((course) => (
          <div
            className="row border rounded my-2 pointcursor p-2"
            key={course.id}
          >
            <div className="col-sm">
              <Link to={`/courses/${course.id}`}>
                <h4 className="text-primary d-inline-block">{course.title}</h4>
              </Link>
              {course.isNew && (
                <span className="badge bg-primary mx-2">New</span>
              )}
              <p>{course.shortDesc}</p>
            </div>
          </div>
        ))}
        {courses.length === 0 && (
          <div className="text-center  justify-content-center align-content-center px-5 m-5">
            <h4 className="display-4 px-5 mx-5">No Courses Available</h4>
          </div>
        )}
      </div>
    </>
  );
};

export default CoursesPage;
