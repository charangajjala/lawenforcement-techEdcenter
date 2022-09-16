import React, { useEffect, useRef, useState } from "react";
import useHttp from "../../../hooks/use-http";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import TableRow from "../../../util/components/TableRow";
import useAlert from "../../../hooks/use-alert";
import FilterInput from "../../../util/components/FilterInput";
import SetAlert from "../../../util/components/SetAlert";
import "./CoursePage.css";

const CoursePage = () => {
  const [courses, setCourses] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  const list = ["Home", "Courses"];
  const order = [
    "id",
    "courseNum",
    "title",
    "isActive",
    "isNew",
    "created",
    "createdBy",
  ];
  useEffect(() => {
    sendRequest({ url: "/courses/" }, setCourses).catch((e) => {});
  }, [sendRequest]);

  const del = async (id) => {
    const delCourseNum = courses.find((course) => course.id === id).courseNum;
    if (window.confirm(`Is it okay to delete course ${delCourseNum}`)) {
      try {
        await sendRequest({ method: "DELETE", url: `/courses/${id}` }, null);
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "/courses/" }, setCourses);
      } catch (error) {}
    }
  };

  const scid = useRef({ value: "" });
  const stitle = useRef({ value: "" });
  const sactive = useRef({ value: "" });
  const snew = useRef({ value: "" });
  const screatedat = useRef({ value: "" });

  const resetFilters = (e) => {
    scid.current.value = "";
    stitle.current.value = "";
    sactive.current.value = "";
    snew.current.value = "";
    screatedat.current.value = "";
    formref.current.reset();
  };

  const searchHandler = (e) => {
    if (e) e.preventDefault();
    const params = {
      scid: scid.current.value,
      stitle: stitle.current.value,
      sactive: sactive.current.value,
      snew: snew.current.value,
      screatedat: screatedat.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/courses/", params }, setCourses);
    } catch (error) {}
  };

  const formref = useRef();

  const filtcol = "col-2";
  return (
    <div className="container-fluid p-4  ">
      <BreadCrumbs list={list} addEntity={"course"} />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <FilterInput label="Course Id" col={filtcol} filtref={scid} />
          <FilterInput label="Course Title" col={filtcol} filtref={stitle} />
          <FilterInput
            col={filtcol}
            type="select"
            options={["-Active-", "true", "false"]}
            filtref={sactive}
          />
          <FilterInput
            col={filtcol}
            type="select"
            options={["-New-", "true", "false"]}
            filtref={snew}
          />
          <FilterInput col={filtcol} type="date" filtref={screatedat} />
          <div className="col-2 m-1">
            <button type="submit" className="btn btn-primary">
              Search
            </button>
            <button
              type="button"
              className="btn btn-primary mx-3"
              onClick={resetFilters}
            >
              Reset
            </button>
          </div>
        </div>
      </form>
      <table className="table  table-striped m-2 ">
        <thead>
          <tr>
            <th scope="col">Course Id</th>
            <th scope="col">Title</th>
            <th scope="col">Active</th>
            <th scope="col">New</th>
            <th scope="col">Created</th>
            <th scope="col">Created By</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {courses.map((course) => (
            <TableRow
              key={course.id}
              data={course}
              path="courses"
              del={del}
              order={order}
            />
          ))}
          
        </tbody>
      </table>
      {courses.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Courses Available</h4>
            </div>
          )}
    </div>
  );
};

export default CoursePage;
