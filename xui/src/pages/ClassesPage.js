import React, { useState, useEffect, useRef, useMemo } from "react";
import { Link } from "react-router-dom";
import BreadCrumbs from "../util/components/BreadCrumbs";
import useHttp from "../hooks/use-http";
import FilterInput from "../util/components/FilterInput";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";
import { selectStates, selectMonths } from "../constants/selectConstants";

const ClassesPage = () => {
  const [classes, setClasses] = useState([]);
  const [courses, setCourses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [hosts, setHosts] = useState([]);
  const [locations, setLocations] = useState([]);
  const list = ["Home", "Classes"];
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    async function fetch() {
      try {
        await sendRequest({ url: "/classes/" }, setClasses);
        await sendRequest({ url: "/instructors/team/" }, setInstructors);
        await sendRequest({ url: "/hosts/locations/" }, setLocations);
        await sendRequest({ url: "/hosts/filterlist/" }, setHosts);
        await sendRequest({ url: "/courses/" }, setCourses);
      } catch (error) {}
    }
    fetch();
  }, [sendRequest]);

  const selectTransformUsers = useMemo(
    () =>
      instructors.map((user) => {
        return { id: user.id, username: `${user.firstName} ${user.lastName}` };
      }),
    [instructors]
  );

  const scourse = useRef({ value: "" });
  const sinstructor = useRef({ value: "" });
  const shost = useRef({ value: "" });
  const slocation = useRef({ value: "" });
  const smonth = useRef({ value: "" });
  const sstate = useRef({ value: "" });

  const resetFilters = (e) => {
    scourse.current.value = "";
    sinstructor.current.value = "";
    shost.current.value = "";
    slocation.current.value = "";
    smonth.current.value = "";
    sstate.current.value = "";
    formref.current.reset();
  };

  const formref = useRef();

  const searchHandler = (e) => {
    if (e) e.preventDefault();

    const params = {
      scourse: scourse.current.value,
      sinstructor: sinstructor.current.value,
      shost: shost.current.value,
      slocation: slocation.current.value,
      smonth: smonth.current.value,
      sstate: sstate.current.value,
    };

    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/classes/", params: params }, setClasses);
    } catch (error) {}
  };

  return (
    <>
      <BreadCrumbs list={list} title="Training Schedule" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <div className="container ">
        <form
          className="form-inline py-3 mb-3 border rounded"
          onSubmit={searchHandler}
          ref={formref}
        >
          <td>
            <FilterInput
              label="-Course-"
              filtref={scourse}
              options={courses}
              val="id"
              show="title"
              col="m-2"
            />
          </td>
          <td>
            <FilterInput
              label="-Instructor-"
              filtref={sinstructor}
              options={selectTransformUsers}
              val="id"
              show="username"
              col="m-2"
            />
          </td>
          <td>
            <FilterInput
              label="-Host-"
              filtref={shost}
              options={hosts}
              val="id"
              show="name"
              col="m-2"
            />
          </td>
          <td>
            <FilterInput
              label="-Host Location-"
              filtref={slocation}
              options={locations}
              val="id"
              show="name"
              col="m-2"
            />
          </td>

          <td>
            {" "}
            <FilterInput
              label="-Month-"
              filtref={smonth}
              options={selectMonths}
              val="value"
              show="name"
              col="m-2"
            />
          </td>
          <td>
            <FilterInput
              label="-State-"
              filtref={sstate}
              options={selectStates}
              val="value"
              show="name"
              col="m-2"
            />
          </td>

          <td className="align-middle">
            <input
              type="submit"
              className="btn btn-primary m-2"
              name="search"
              value="Search"
            />
          </td>

          <td className="align-middle">
            <button
              type="button"
              className="btn btn-primary mx-3"
              onClick={resetFilters}
            >
              Reset
            </button>
          </td>
        </form>

        <table className="table table-borderless table-striped table-sm ">
          <tr className="border bg-primary text-white ">
            <th>Course</th>
            <th>Instructor</th>
            <th>Host</th>
            <th>Location</th>
            <th>Dates</th>
            <th>Fee</th>
            <th></th>
          </tr>
          <tbody>
            {classes.map((cls) => (
              <tr key={cls.id}>
                <td>
                  <Link to={`/classes/${cls.id}`}>{cls.course}</Link>
                </td>
                <td>{cls.instructor}</td>
                <td>{cls.host || "Not Applicable"}</td>
                <td>{cls.location || "Not Applicable"}</td>
                <td>{`${cls.startDate} to ${cls.endDate}`}</td>
                <td>{`$${cls.fee}`}</td>
                <td>
                  <Link to={`/classes/${cls.id}`}>Register</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {classes.length === 0 && (
          <div className="text-center  justify-content-center align-content-center px-5 m-5">
            <h4 className="display-4 px-5 mx-5">No Classes Available</h4>
          </div>
        )}
      </div>

      <br />
      <div className="row"></div>
    </>
  );
};

export default ClassesPage;
