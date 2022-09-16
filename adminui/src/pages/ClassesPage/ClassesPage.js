import React, { useState, useEffect, useRef } from "react";
import useHttp from "../../hooks/use-http";
import useAlert from "../../hooks/use-alert";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import TableRow from "../../util/components/TableRow";
import SetAlert from "../../util/components/SetAlert";
import {
  selectClassStatus,
  selectClassType,
} from "../../constants/selectConstants";
import FilterInput from "../../util/components/FilterInput";

const ClassesPage = () => {
  const [classes, setClasses] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  const list = ["Home", "Classes"];
  const order = [
    "id",
    "course",
    "instructor",
    "host",
    "location",
    "startDate",
    "endDate",
    "status",
    "type",
    "students",
    "flight",
    "car",
    "hotel",
    "material",
  ];

  useEffect(() => {
    sendRequest({ url: "/classes/" }, setClasses).catch((err) => {});
  }, [sendRequest]);

  const del = async (id) => {
    if (window.confirm(`Is it okay to delete the Class `)) {
      try {
        await sendRequest({ method: "DELETE", url: `/classes/${id}` }, null);
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "/classes/" }, setClasses);
      } catch (error) {}
    }
  };

  const filtcol = "col-2";
  const sid = useRef({ value: "" });
  const scname = useRef({ value: "" });
  const siname = useRef({ value: "" });
  const shname = useRef({ value: "" });
  const slocation = useRef({ value: "" });
  const sstartdate = useRef({ value: "" });
  const senddate = useRef({ value: "" });
  const sstatus = useRef({ value: "" });
  const stype = useRef({ value: "" });
  const [clsradio, setClsRadio] = useState("");
  const formref = useRef();

  const onRadioChange = (e) => {
    setClsRadio(e.target.value);
  };

  const resetFilters = (e) => {
    sid.current.value = "";
    scname.current.value = "";
    siname.current.value = "";
    shname.current.value = "";
    slocation.current.value = "";
    sstartdate.current.value = "";
    senddate.current.value = "";
    sstatus.current.value = "";
    stype.current.value = "";
    setClsRadio("");
    formref.current.reset();
  };

  console.log("newherenew", sid.current.value);

  const searchHandler = (e) => {
    if (e) e.preventDefault();
    const params = {
      sid: sid.current.value,
      scname: scname.current.value,
      siname: siname.current.value,
      shname: shname.current.value,
      slocation: slocation.current.value,
      sstartdate: sstartdate.current.value,
      senddate: senddate.current.value,
      sstatus: sstatus.current.value,
      stype: stype.current.value,
      scls: clsradio,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/classes/", params }, setClasses);
    } catch (error) {}
  };

  return (
    <div className="container-fluid p-4">
      <BreadCrumbs list={list} addEntity="cls" addBtnName="Class" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <div className="col-sm-auto">
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio1"
                value="current"
                checked={clsradio === "current"}
                onChange={(e) => {
                  e.persist();
                  onRadioChange(e);
                }}
              />
              <label class="form-check-label" for="inlineRadio1">
                Current
              </label>
            </div>
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio2"
                value="past"
                checked={clsradio === "past"}
                onChange={(e) => {
                  e.persist();
                  onRadioChange(e);
                }}
              />
              <label class="form-check-label" for="inlineRadio2">
                Past
              </label>
            </div>
          </div>
        </div>
        <div className="row">
          <FilterInput label="Class Id" col={filtcol} filtref={sid} />
          <FilterInput label="Course Name" col={filtcol} filtref={scname} />
          <FilterInput label="Instructor Name" col={filtcol} filtref={siname} />
          <FilterInput label="Host Name" col={filtcol} filtref={shname} />
          <FilterInput label="Location" col={filtcol} filtref={slocation} />

          <FilterInput
            col={filtcol}
            type="date"
            filtref={sstartdate}
            label="Start Date"
          />
          <FilterInput
            col={filtcol}
            val="status"
            show="status"
            label="-Status-"
            options={selectClassStatus}
            filtref={sstatus}
          />
          <FilterInput
            col={filtcol}
            val="type"
            show="type"
            label="-Type-"
            options={selectClassType}
            filtref={stype}
          />

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
            <th scope="col">Id</th>
            <th scope="col">Course Name</th>
            <th scope="col">Instructor Name</th>
            <th scope="col">Host Name</th>
            <th scope="col">Location</th>
            <th scope="col">Start Date</th>
            <th scope="col">End Date</th>
            <th scope="col">Status</th>
            <th scope="col">Type</th>
            <th scope="col">Students</th>
            <th scope="col">Flight</th>
            <th scope="col">Car</th>
            <th scope="col">Hotel</th>
            <th scope="col">material</th>
          </tr>
        </thead>
        <tbody>
          {classes.map((cls) => (
            <TableRow
              key={cls.id}
              data={cls}
              path="classes"
              del={del}
              order={order}
            />
          ))}
        </tbody>
      </table>
      {classes.length === 0 && (
        <div className="text-center  justify-content-center align-content-center px-5 m-5">
          <h4 className="display-4 px-5 mx-5">No Classes Available</h4>
        </div>
      )}
    </div>
  );
};

export default ClassesPage;
