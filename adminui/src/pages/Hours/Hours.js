import React, { useState, useEffect, useRef, useCallback } from "react";
import useInput from "../../hooks/use-input";
import useHttp from "../../hooks/use-http";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import {
  checkAddEmpty,
  getData,
} from "../../util/helper-functions/util-functions";

import SelectOne from "../../util/components/SelectOne";
import { selectHourType, selectMonths } from "../../constants/selectConstants";
import Modal from "../../util/components/Modal";

const Hours = () => {
  console.log("-------Hours-------");
  const [hours, setHours] = useState([]);
  const [noDays, setNoDays] = useState();
  const list = ["Home", "Hours"];
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const [parammonth, setParamMonth] = useState("");
  const [paramyear, setParamYear] = useState("");

  useEffect(() => {
    const currentDate = new Date();
    const noDays = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() + 1,
      0
    ).getDate();
    setNoDays(noDays);
    setParamYear(currentDate.getFullYear());
    const parammnth = selectMonths.find(
      (x) => x.mnthnum === currentDate.getMonth()
    ).value;
    setParamMonth(parammnth);
  }, []);

  useEffect(() => {
    const fetch = async () => {
      try {
        await sendRequest({ url: `/hours/` }, setHours);
      } catch (error) {
        //handle
      }
    };
    fetch();
  }, [sendRequest]);

  useEffect(() => {
    if (!!parammonth && !!paramyear) {
      const params = {
        month: parammonth,
        year: parseInt(paramyear),
      };
      for (const k in params) {
        const val = params[k];
        if (val === null || val === undefined || val === "") delete params[k];
      }
      const mnth = selectMonths.find((x) => x.value === parammonth).mnthnum;
      const noDays = new Date(parseInt(paramyear), mnth + 1, 0).getDate();
      setNoDays(noDays);
      console.log(params);
      try {
        sendRequest({ url: "/hours/", params }, setHours);
      } catch (error) {}
    }
  }, [parammonth, paramyear, sendRequest]);

  const topDatejsx = (day) => {
    const hour = hours.find((h) => new Date(h.date).getDate() === day);
    if (hour)
      return (
        <div className="col-sm m-0 p-0" key={day}>
          {" "}
          <DateCard hour={hour} setHours={setHours} mod="EDIT" />
        </div>
      );
    else {
      const mnthnum = selectMonths.find((x) => x.value === parammonth)?.mnthnum;
      const date = new Date(parseInt(paramyear), mnthnum, day);
      return (
        <div className="col-sm m-0 p-0" key={day}>
          <DateCard hour={hour} setHours={setHours} mod="ADD" date={date} />
        </div>
      );
    }
  };

  const jsx = () => {
    if (parammonth && paramyear) {
      const mnthnum = selectMonths.find((x) => x.value === parammonth).mnthnum;
      const date = new Date(parseInt(paramyear), mnthnum, 1);
      const diff = date.getDay();
      console.log("diff", diff);
      let arr1 = [];
      let arr2 = [];
      for (let i = 1; i <= 7; i++) {
        if (i <= diff) {
          arr2.push(
            <div className="col-sm m-0 p-0 card">
              <div className="w-100 h-100 bg-light"></div>
            </div>
          );
        } else {
          // date card with date= i-diff
          console.log("diff", diff);
          arr2.push(topDatejsx(i - diff));
        }
      }
      arr1.push(<div className="row p-0 m-0">{arr2}</div>);
      for (let i = 7 - diff + 1; i <= 35; ) {
        let arr = [];
        for (let j = 1; j <= 7; j++, i++) {
          if (i > noDays) {
            arr.push(
              <div className="col-sm m-0 p-0">
                <div className="w-100 h-100"></div>
              </div>
            );
          } else {
            arr.push(topDatejsx(i));
          }
        }
        arr1.push(<div className="row p-0 m-0">{arr}</div>);
      }
      return arr1;
    }
  };

  return (
    <>
      <div className="container p-5">
        <BreadCrumbs list={list} />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />

        <div className="row">
          <div className="col-2">
            <input
              type="number"
              placeholder="Year"
              value={paramyear}
              onChange={(e) => {
                setParamYear(e.target.value);
              }}
              className="form-control"
            />
          </div>
          <div className="col-2">
            {" "}
            <select
              value={parammonth}
              onChange={(e) => {
                setParamMonth(e.target.value);
              }}
              className="form-select"
            >
              {selectMonths.map((x) => {
                return (
                  <option value={x.value} key={x.value}>
                    {x.name}
                  </option>
                );
              })}
            </select>
          </div>
        </div>

        <div className="container my-3">
          <div className="row p-0 ">
            <div className="row m-0 p-0 ">
              <div className="col-sm text-white  p-0 m-0 bg-dark text-center   ">
                <h5 className="mx-5">Sun</h5>
              </div>
              <div className="col-sm text-white  p-0 m-0 bg-dark text-center ">
                <h5 className="mx-5">Mon</h5>
              </div>
              <div className="col-sm text-white  p-0 m-0 bg-dark text-center ">
                <h5 className="mx-5">Tue</h5>
              </div>
              <div className="col-sm text-white  p-0 m-0 bg-dark text-center ">
                <h5 className="mx-5">Wed</h5>
              </div>
              <div className="col-sm text-white  p-0 m-0 bg-dark text-center ">
                <h5 className="mx-5">Thu</h5>
              </div>
              <div className="col-sm text-white  p-0 m-0 bg-dark text-center ">
                <h5 className="mx-5">Fri</h5>
              </div>
              <div className="col-sm text-white  p-0 m-0 bg-dark text-center ">
                <h5 className="mx-5">Sat</h5>
              </div>
            </div>

            {jsx()}
          </div>
        </div>
      </div>
    </>
  );
};

const HourModal = ({ closeFunc, hour, mod, setClose, date }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const useInputInit = (initval) => (mod === "EDIT" ? initval : null);

  const [hours, hoursHandler] = useInput(
    useInputInit(hour ? hour.hours : null)
  );
  const cb = useCallback(getData, []);
  const type = useRef("");
  const getDateString = (d) => {
    let mnthnum = d.getMonth() + 1;
    if (mnthnum < 10) mnthnum = `0${mnthnum}`;
    return `${d.getFullYear()}-${mnthnum}-${d.getDate()}`;
  };
  const submit = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    const body = {
      type: type.current,
      hours: parseInt(hours),
    };
    checkAddEmpty(body);

    body.date = mod === "EDIT" ? hour.date : getDateString(date);

    try {
      if (mod === "ADD")
        await sendRequest({ url: `/hours/`, method: "POST", body });
      if (mod === "EDIT")
        await sendRequest({
          url: `/hours/`,
          method: "PUT",
          body,
        });
      setShowAlert(true);
      setAlertMessage("Successfully saved");
      closeFunc.current = closeFunc.current.bind(null, body);
      setClose(true);
    } catch (error) {}
  };
  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={submit}>
        <div>
          {" "}
          <h3>Hours</h3>{" "}
          <input
            type="number"
            value={hours}
            onChange={hoursHandler}
            max="24"
            className="form-control"
          />
        </div>

        <SelectOne
          col={""}
          cb={cb}
          cbref={type}
          selectEntitys={selectHourType}
          data={hour ? hour.type : undefined}
          comp="type"
          show="type"
          val="type"
          title="Type"
        />
        <input type="submit" value="Submit" className="btn btn-primary my-2" />
      </form>
    </div>
  );
};

const DateCard = ({ hour, setHours, mod, date }) => {
  const [close, setClose] = useState(false);
  const closeFunc = useRef((body) => {
    setHours((prev) => {
      const arr = prev.filter((x) => x.date !== body.date);
      arr.push(body);
      return [...arr];
    });
    setClose(false);
  });

  return (
    <div
      className="card text-dark bg-light w-100 h-100 "
      type="button"
      data-toggle={"modal"}
      data-backdrop="static"
      data-keyboard="false"
      data-target={`#exampleModalLong${hour ? hour.date : date.toString()}`}
    >
      <div className="m-2">
        <h6>{hour ? new Date(hour.date).getDate() : date.getDate()}</h6>
      </div>
      <div className="card-body">
        {mod !== "ADD" && (
          <div>
            <h4>Hours : {hour.hours}</h4>
            <h4>
              <span className="badge bg-dark">{hour.type}</span>
            </h4>
          </div>
        )}

        <Modal
          Component={HourModal}
          props={{ hour, date, closeFunc, setClose, mod }}
          thisModal={hour ? hour.date : date.toString()}
          addBtnName={mod === "ADD" ? "Add" : "Edit"}
          onClose={(_) => {
            if (close) {
              closeFunc.current();
            }
          }}
          nobutton={true}
        />
      </div>
    </div>
  );
};

export default Hours;
