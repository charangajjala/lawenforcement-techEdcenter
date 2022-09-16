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
  checkAddEmpty,
  checkIfEdited,
  getData,
} from "../../util/helper-functions/util-functions";

import FileUpload from "../../util/components/FileUpload";
import SelectOne from "../../util/components/SelectOne";
import {
  selectClassStatus,
  selectClassType,
  selectClassDeliveryType,
} from "../../constants/selectConstants";
import Notes from "../../util/components/Notes";
import Desc from "../../util/components/Desc";
import Modal from "../../util/components/Modal";
import Papa from "papaparse";

const AAR = ({ aar }) => {
  const questions = ["q1", "q2"];
  return (
    <div>
      {aar &&
        questions.map((q, i) => {
          return (
            <div key={i}>
              <h3>{q}</h3>
              Answer : {aar[i]}
            </div>
          );
        })}
    </div>
  );
};

const Evaluations = ({ evaluations }) => {
  const questions = ["q1", "q2"];

  const calAvg = (i) => {
    let sum = 0;
    for (const evaluation of evaluations) {
      sum += evaluation[`q${i}`];
    }
    return (sum / evaluations.length).toFixed(2);
  };

  const calPercent = (i) => {
    let trueCount = 0;
    for (const evaluation of evaluations) {
      console.log(`q${i}`, evaluation[`q${i}`]);
      if (evaluation[`q${i}`] === true) trueCount++;
    }
    console.log("trueCount", trueCount);
    console.log("evaluations.length", evaluations.length);
    return ((trueCount / evaluations.length) * 100).toFixed(2);
  };

  return (
    <div>
      {evaluations && (
        <table className="table table-striped">
          <thead>
            <tr>
              <th scope="col">Question</th>
              <th scope="col">Ratings</th>
              <th scope="col">Avergae Rating</th>
            </tr>
          </thead>
          <tbody>
            {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => {
              return i < 9 ? (
                <tr key={i}>
                  <td>{questions[i]}</td>
                  <td>
                    {evaluations.map(
                      (evaluation) => ` ${evaluation[`q${i + 1}`]},`
                    )}
                  </td>

                  <td>{calAvg(i + 1)}</td>
                </tr>
              ) : (
                <tr key={i}>
                  <td>{questions[i]}</td>
                  <td>
                    {evaluations.map(
                      (evaluation) => ` ${evaluation[`q${i + 1}`]},`
                    )}
                  </td>
                  <td>
                    {`True : ${calPercent(i + 1)}% False : ${
                      100 - calPercent(i + 1)
                    }%`}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
};

const Move = ({ studentId, clsid, selectClasses, setRefresh }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const cb = useCallback(getData, []);
  const destclassid = useRef("");
  const submit = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      await sendRequest({
        url: `/classes/move/${clsid}`,
        method: "POST",
        body: { studentId, destClassId: parseInt(destclassid.current) },
      });
      setShowAlert(true);
      setAlertMessage("Moved the Student Successfully");
      setRefresh(true);
    } catch (error) {}
  };
  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={submit}>
        <SelectOne
          col={"col-md-6"}
          cb={cb}
          cbref={destclassid}
          selectEntitys={selectClasses}
          val="id"
          show="id"
          comp="id"
          title="Select Destination Class"
          initTxt="-Select Class-"
        />
        <input type="submit" className="btn btn-primary" value="Move" />
      </form>
    </div>
  );
};

const RosterTable = ({ studentss, selectClasses, clsid, upload }) => {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    setStudents(studentss);
  }, [studentss]);

  const [refresh, setRefresh] = useState(false);

  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  const Substitute = ({ studentId }) => {
    const [showAlert, setShowAlert, alertMessage, setAlertMessage] =
      useAlert(true);
    const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
    const newStudentId = useRef("");

    const submit = async (e) => {
      e.preventDefault();
      e.stopPropagation();
      try {
        await sendRequest({
          url: `/classes/substitute/${clsid}`,
          method: "POST",
          body: {
            studentId,
            newStudentId: parseInt(newStudentId.current.value),
          },
        });
        setShowAlert(true);
        setAlertMessage("Substituted the Student Successfully");
      } catch (error) {}
    };

    return (
      <div>
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form onSubmit={submit}>
          <input
            type="text"
            placeholder={"Enter Replacing Student Id"}
            ref={newStudentId}
            required
          />
          <input type="submit" className="btn btn-primary" value="Substitute" />
        </form>
      </div>
    );
  };

  const remove = async (studentId) => {
    if (window.confirm(`Is it okay to remove the student from the class?`)) {
      try {
        await sendRequest(
          {
            method: "POST",
            url: `/classes/remove/${clsid}`,
            body: { studentId },
          },
          null
        );
        setShowAlert(true);
        setAlertMessage("Removed the Student Successfully");
        setStudents((prev) => {
          return prev.filter((s) => s.id !== studentId);
        });
      } catch (error) {}
    }
  };

  const markPresent = async (studentId) => {
    try {
      await sendRequest(
        {
          method: "POST",
          url: `/classes/signin/${clsid}`,
          body: { studentId },
        },
        null
      );
      setShowAlert(true);
      setAlertMessage("Marked the Student as Present Successfully");
      setStudents((prev) => {
        prev.find((s) => s.id === studentId).attendance = true;
        return [...prev];
      });
    } catch (error) {}
  };

  const sendEval = async (studentId) => {
    try {
      await sendRequest(
        {
          method: "POST",
          url: `/classes/sendEvaluation/${clsid}`,
          body: { studentId },
        },
        null
      );
      setShowAlert(true);
      setAlertMessage("Sent the Evaluation Email Successfully");
      setStudents((prev) => {
        prev.find((s) => s.id === studentId).evaluation = null;
        return [...prev];
      });
    } catch (error) {}
  };

  return (
    <div>
      {!upload && (
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      )}
      <table className="table table-borderless table-striped table-sm">
        <thead>
          {" "}
          <tr className="border bg-primary text-white">
            {!upload && <th>Student Id</th>}
            <th>Title</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Phone</th>
            {!upload && <th>Agency</th>}
            {!upload && <th></th>}
          </tr>
        </thead>
        <tbody>
          {students.map((student, i) => {
            const signedin = student.attendance;
            const iseval = student.evaluation;
            return (
              <tr key={i}>
                {!upload && <td>{student.id}</td>}
                <td>{student.title}</td>
                <td>{student.firstName}</td>
                <td>{student.lastName}</td>
                <td>{student.email}</td>
                <td>{student.phone}</td>
                {!upload && <td>{student.agency}</td>}
                {!upload && (
                  <td>
                    {!signedin && (
                      <>
                        <Modal
                          addBtnName="Move"
                          Component={Move}
                          thisModal={`Move${student.id}`}
                          props={{
                            studentId: student.id,
                            clsid,
                            selectClasses,
                            setStudents,
                            setRefresh,
                          }}
                          onClose={() => {
                            if (refresh) {
                              setStudents((prev) => {
                                return prev.filter((s) => s.id !== student.id);
                              });
                              setRefresh(false);
                            }
                          }}
                        />

                        <Modal
                          addBtnName="Substitute"
                          Component={Substitute}
                          props={{ studentId: student.id }}
                          thisModal={`Substitute${student.id}`}
                        />
                        <button
                          type="button"
                          className="btn btn-danger btn-sm"
                          onClick={(_) => {
                            remove(student.id);
                          }}
                        >
                          Remove
                        </button>
                        <button
                          type="button"
                          className={`btn ${`btn-primary`} btn-sm`}
                          onClick={(_) => {
                            markPresent(student.id);
                          }}
                          disabled={!!signedin}
                        >
                          {signedin ? "Present" : "Mark Present"}
                        </button>
                      </>
                    )}

                    <button
                      type="button"
                      className={`btn btn-primary btn-sm`}
                      disabled={iseval === null || iseval}
                      onClick={(e) => {
                        sendEval(student.id);
                      }}
                    >
                      {iseval === null
                        ? "Sent Email"
                        : iseval
                        ? "Evaluated"
                        : "Send Email"}
                    </button>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

const RosterUploadModal = ({ clsid }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] =
    useAlert(true);
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const [rosterdata, setRosterData] = useState([]);
  const [loading, setLoading] = useState(false);
  const rosterfile = useRef();

  const confirmData = (result) => {
    const closeUpload = (str) => {
      alert(str);
      rosterfile.current.value = null;
      setLoading(false);
    };
    const reqfields = [
      "title",
      "firstname",
      "lastname",
      "email",
      "phone",
      "agency",
    ];
    const givenfields = result.meta.fields;
    console.log("givenfields", givenfields);
    const containsAll = givenfields.every((f) =>
      reqfields.includes(f.toLowerCase())
    );
    if (!containsAll) {
      closeUpload(
        "Extra fields found in the file. Please remove them and try again."
      );
      return;
    }
    if (givenfields.filter((f) => f.toLowerCase() !== "title").length < 5) {
      closeUpload(
        "Either  First Name or Last Name or Email or Phone is missing. Please check the file and try again."
      );
      return;
    }
    const data = result.data;
    console.log("csvdata", data);
    const novalidfields = [];
    for (const field of givenfields) {
      //check data validation
      if (field.toLowerCase() !== "title") {
        for (const row of data) {
          if (
            row[field] === undefined ||
            row[field] === null ||
            row[field] === ""
          ) {
            novalidfields.push(field.toLowerCase());
          }
        }
      }
    }
    if (novalidfields.length > 0) {
      let string = "Some data is missing in the following fields: ";
      for (const field of [...new Set(novalidfields)]) {
        string = string + field + " ";
      }
      closeUpload(string);
      return;
    }
    const newdata = [];
    for (const row of data) {
      const keys = Object.keys(row);
      let newobj = {};
      for (const k of keys) {
        if (k.toLowerCase() === "firstname") {
          newobj["firstName"] = row[k];
        } else if (k.toLowerCase() === "lastname") {
          newobj["lastName"] = row[k];
        } else newobj[k.toLowerCase()] = row[k];
      }
      newdata.push(newobj);
    }
    setLoading(false);
    setRosterData(newdata);
  };

  const rosterUpload = (e) => {
    e.preventDefault();
    e.stopPropagation();

    const file = rosterfile.current.files[0];
    if (!file) return;
    console.log("file", file);
    const types = [
      "application/vnd.ms-excel",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/csv",
    ];
    if (!types.includes(file.type)) {
      alert("Only .csv, .xls, .xlsx files are allowed");
      return;
    }
    setLoading(true);
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: confirmData,
      error: (e) => {
        setShowAlert(true);
        setAlertMessage({ e: true, message: "Error in parsing the file" });
        setLoading(false);
        console.log(e);
      },
    });
  };

  const submitRoster = async (e) => {
    e.preventDefault();
    try {
      await sendRequest({
        url: `classes/inServiceRoster/${clsid}/`,
        method: "POST",
        body: rosterdata,
      });
      setShowAlert(true);
      setAlertMessage("Roster uploaded successfully");
    } catch (error) {}
  };

  return (
    <div>
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={submitRoster}>
        <form onSubmit={rosterUpload}>
          <input
            type="file"
            required
            ref={rosterfile}
            // accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, "
          />
          <input type="submit" className="btn btn-primary" value="Upload" />
        </form>
        {loading && <div>Loading the File, Please wait...</div>}
        {rosterdata.length > 0 && !loading && (
          <div>
            <h4>Preview the Roster and Confirm</h4>
            <RosterTable upload={true} studentss={rosterdata} />
            <input type="submit" className="btn btn-primary" value="Confirm" />
          </div>
        )}
      </form>
    </div>
  );
};

const ClassDetailPage = ({ mode }) => {
  console.log("-------ClassDetailPage-------");
  const [cls, setClass] = useState({});
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectCourses, setSelectCourses] = useState([]);
  const [selectInstructors, setSelectInstructors] = useState([]);
  const [selectLocations, setSelectLocations] = useState([]);
  const [selectHosts, setSelectHosts] = useState([]);
  const [selectClasses, setSelectClasses] = useState([]);
  const [selectInserviceInvoices, setSelectInserviceInvoices] = useState([]);

  const list =
    mode === "EDIT"
      ? ["Home", "Classes", `${cls.id}`]
      : ["Home", "Classes", ""];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  const selectTransformInstructors = useMemo(
    () =>
      selectInstructors.map((instructor) => {
        return {
          id: instructor.id,
          instructorname: `${instructor.firstName} ${instructor.lastName}`,
        };
      }),
    [selectInstructors]
  );

  useEffect(() => {
    const fetch = async () => {
      console.log("inside fetch");
      try {
        if (mode === "EDIT") {
          console.log("check", params.id);
          await sendRequest({ url: `/classes/${params.id}` }, setClass);
        }
        await sendRequest({ url: "/courses/" }, setSelectCourses, true);
        await sendRequest({ url: "/instructors/" }, setSelectInstructors, true);
        await sendRequest(
          { url: "/hosts/locations/" },
          setSelectLocations,
          true
        );
        await sendRequest({ url: "/hosts/" }, setSelectHosts, true);
        await sendRequest({ url: "/classes/" }, setSelectClasses);
        await sendRequest(
          { url: "/invoice/" },
          setSelectInserviceInvoices,
          true
        );
      } catch (error) {
        //handle
      }
    };
    fetch();
  }, [mode, params.id, sendRequest]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [startDate, startDateHandler] = useInput(useInputInit(cls.startDate));
  const [endDate, endDateHandler] = useInput(useInputInit(cls.endDate));
  const [startTime, startTimeHandler] = useInput(cls.startTime || "08:00");
  const [endTime, endTimeHandler] = useInput(cls.endTime || "16:00");
  const [earlyFee, earlyFeeHandler] = useInput(useInputInit(cls.earlyFee));
  const [regularFee, regularFeeHandler] = useInput(
    useInputInit(cls.regularFee)
  );
  const [lateFee, lateFeeHandler] = useInput(useInputInit(cls.lateFee));
  const [inserviceFee, inserviceFeeHandler] = useInput(
    useInputInit(cls.inserviceFee)
  );

  const [inserviceSeats, inserviceSeatsHandler] = useInput(
    useInputInit(cls.inserviceSeats)
  );
  const [onlineMeetingDetails, onlineMeetingDetailsHandler] = useInput(
    useInputInit(cls.onlineMeetingDetails)
  );
  const [orderDate, orderDateHandler] = useInput(useInputInit(cls.orderDate));
  const [orderDeliveryDate, orderDeliveryDateHandler] = useInput(
    useInputInit(cls.orderDeliveryDate)
  );
  const [orderTrackingNumber, orderTrackingNumberHandler] = useInput(
    useInputInit(cls.orderTrackingNumber)
  );
  const [orderCarrier, orderCarrierHandler] = useInput(
    useInputInit(cls.orderCarrier)
  );
  const [orderQuantity, orderQuantityHandler] = useInput(
    useInputInit(cls.orderQuantity)
  );
  const [orderPrice, orderPriceHandler] = useInput(
    useInputInit(cls.orderPrice)
  );
  const [orderNotes, orderNotesHandler] = useInput(
    useInputInit(cls.orderNotes)
  );
  const [postedOnPTT, postedOnPTTHandler] = useInput(
    useInputInit(cls.postedOnPTT),
    "checkbox"
  );
  const [flightPrice, flightPriceHandler] = useInput(
    useInputInit(cls.flightPrice)
  );
  const [flightInfo, flightInfoHandler] = useInput(
    useInputInit(cls.flightInfo)
  );
  const [carRentalPrice, carRentalPriceHandler] = useInput(
    useInputInit(cls.carRentalPrice)
  );
  const [carRentalInfo, carRentalInfoHandler] = useInput(
    useInputInit(cls.carRentalInfo)
  );
  const [hotelPrice, hotelPriceHandler] = useInput(
    useInputInit(cls.hotelPrice)
  );
  const [hotelInfo, hotelInfoHandler] = useInput(useInputInit(cls.hotelInfo));
  const course = useRef("");
  const location = useRef("");
  const host = useRef("");
  const instructor = useRef("");
  const inserviceInvoice = useRef("");

  const docs = useRef([]);
  const adminDocs = useRef([]);
  const status = useRef("");
  const type = useRef("");
  const deliveryType = useRef("");
  const adminNotes = useRef([]);

  const cb = useCallback(getData, []);
  const col = "col-md-4";

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Class `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/classes/${cls.id}` },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {}
    }
  };

  const submitHandler = async (e) => {
    if (e) {
      e.preventDefault();
    }

    const setDocId = (doc, id) => {
      doc.id = id.id;
    };

    try {
      for (const doc of docs.current) {
        if (doc.old !== true && doc.action === "ADD") {
          await fileRequest(
            { url: "/file/", method: "POST", body: doc.file },
            setDocId.bind(null, doc),
            doc.name
          );
        }
      }

      for (const doc of adminDocs.current) {
        if (doc.old !== true && doc.action === "ADD") {
          await fileRequest(
            { url: "/file/", method: "POST", body: doc.file },
            setDocId.bind(null, doc),
            doc.name
          );
        }
      }

      const newClass = {
        course: parseInt(course.current),
        instructor: parseInt(instructor.current),
        host: parseInt(host.current),
        location: parseInt(location.current),
        status: status.current,
        type: type.current,
        deliveryType: deliveryType.current,
        inserviceInvoice: parseInt(inserviceInvoice.current),
        startDate,
        endDate,
        startTime,
        endTime,
        earlyFee,
        lateFee,
        inserviceFee,
        regularFee,
        inserviceSeats: parseInt(inserviceSeats),
        onlineMeetingDetails,
        postedOnPTT,
        orderNotes,
        orderDate,
        orderPrice,
        orderQuantity,
        orderCarrier,
        orderTrackingNumber,
        orderDeliveryDate,
        flightPrice,
        flightInfo,
        carRentalInfo,
        carRentalPrice,
        hotelInfo,
        hotelPrice,
        docs: adjust(docs.current, mode),
        adminDocs: adjust(adminDocs.current, mode),
        adminNotes: adminNotes.current,
      };
      console.log("old", newClass);
      checkAddEmpty(newClass);
      if (mode === "EDIT") {
        checkIfEdited(newClass, cls);
      }
      console.log("new ", newClass);
      if (Object.keys(newClass).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            { method: "POST", url: "/classes/", body: newClass },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/classes/${params.id}`,
              body: newClass,
            },
            null
          );
        console.log("<<<<sent req in submit>>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {
      console.log(error);
    }
  };

  console.log(startTime);

  return (
    <>
      <div className="container-fluid p-5">
        <BreadCrumbs list={list} />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="cd" onSubmit={submitHandler}>
          <div className="row">
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={status}
              selectEntitys={selectClassStatus}
              data={cls.status}
              comp="status"
              show="status"
              val="status"
              title="Status"
              required={true}
              initTxt="Select Status"
            />
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={type}
              selectEntitys={selectClassType}
              data={cls.type}
              comp="type"
              show="type"
              val="type"
              title="Class Type"
              required={true}
              initTxt="Select Type"
            />
            <Col
              col={"col-md"}
              label="Start Date"
              value={startDate}
              onChange={startDateHandler}
              type="date"
              required={true}
            />
            <Col
              col={"col-md"}
              label="End Date"
              value={endDate}
              onChange={endDateHandler}
              type="date"
              required={true}
            />
          </div>
          <div className="row">
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={course}
              data={cls.course}
              selectEntitys={selectCourses}
              val="id"
              show="title"
              comp="id"
              title="Course"
              required={true}
              initTxt="Select Course"
            />
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={instructor}
              data={cls.instructor}
              selectEntitys={selectTransformInstructors}
              val="id"
              show="instructorname"
              comp="id"
              title="Instructor"
              required={true}
              initTxt="Select Instructor"
            />
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={host}
              data={cls.host}
              selectEntitys={selectHosts}
              val="id"
              show="name"
              comp="id"
              title="Host"
              initTxt="-Select Host-"
              required={true}
            />
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={location}
              data={cls.location}
              selectEntitys={selectLocations}
              val="id"
              show="name"
              comp="id"
              title="Host Location"
              initTxt="-Select Host Location-"
            />
          </div>
          <div className="row">
            <Col
              col={"col-md"}
              label="Start Time"
              value={startTime}
              onChange={startTimeHandler}
              type="time"
              required={true}
            />
            <Col
              col={"col-md"}
              label="End Time"
              value={endTime}
              onChange={endTimeHandler}
              type="time"
              required={true}
            />
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={deliveryType}
              selectEntitys={selectClassDeliveryType}
              data={cls.deliveryType}
              comp="type"
              show="type"
              val="type"
              title="Delivery Type"
              initTxt="-Select Delivery Type-"
            />
            <Col
              col={"col-md"}
              label="Posted On PPT"
              value={postedOnPTT}
              onChange={postedOnPTTHandler}
              type="checkbox"
            />
          </div>
          <div className="row">
            <Col
              col={"col-md"}
              label="Early Fee"
              value={earlyFee}
              onChange={earlyFeeHandler}
            />
            <Col
              col={"col-md"}
              label="Late Fee"
              value={lateFee}
              onChange={lateFeeHandler}
            />
            <Col
              col={"col-md"}
              label="Regular Fee"
              value={regularFee}
              onChange={regularFeeHandler}
            />
            <Col
              col={"col-md"}
              label="Online Meeting Details"
              value={onlineMeetingDetails}
              onChange={onlineMeetingDetailsHandler}
              type="textarea"
            />
          </div>
          <div className="row">
            <Col
              col={"col-md"}
              label="Inservice Fee"
              value={inserviceFee}
              onChange={inserviceFeeHandler}
            />
            <Col
              col={"col-md"}
              label="Inservice Seats"
              value={inserviceSeats}
              onChange={inserviceSeatsHandler}
              type="number"
            />
            <SelectOne
              col={"col-md"}
              cb={cb}
              cbref={inserviceInvoice}
              data={cls.inServiceInvoice}
              selectEntitys={selectInserviceInvoices}
              val="invoiceNum"
              show="invoiceNum"
              comp="invoiceNum"
              title="Inservice Invoice"
              initTxt="-Select Inservice Invoice-"
            />
          </div>
          <div className="row">
            <div className="col-md-4">
              <div className="row">
                {" "}
                <Col
                  col={"col-md-6"}
                  label="Order Date"
                  value={orderDate}
                  onChange={orderDateHandler}
                  type="date"
                />
                <Col
                  col={"col-md-6"}
                  label="Order Delivery Date"
                  value={orderDeliveryDate}
                  onChange={orderDeliveryDateHandler}
                  type="date"
                />
                <Col
                  col={"col-md-6"}
                  label="Order Tracking Number"
                  value={orderTrackingNumber}
                  onChange={orderTrackingNumberHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Order Carrier"
                  value={orderCarrier}
                  onChange={orderCarrierHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Order Quantity"
                  value={orderQuantity}
                  onChange={orderQuantityHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Order Price"
                  value={orderPrice}
                  onChange={orderPriceHandler}
                />
                <Col
                  col={"col-md"}
                  label="Order Notes"
                  value={orderNotes}
                  onChange={orderNotesHandler}
                  type="textarea"
                />
              </div>
            </div>
            <div className="col-md">
              <div className="row">
                <Col
                  col={"col-md-12"}
                  label="Flight Price"
                  value={flightPrice}
                  onChange={flightPriceHandler}
                />
                <Col
                  col={"col-md-12"}
                  label="Flight Info"
                  value={flightInfo}
                  onChange={flightInfoHandler}
                  type="textarea"
                  rows="9"
                />
              </div>
            </div>
            <div className="col-md">
              {" "}
              <div className="row">
                {" "}
                <Col
                  col={"col-md-12"}
                  label="Car Rental Price"
                  value={carRentalPrice}
                  onChange={carRentalPriceHandler}
                />
                <Col
                  col={"col-md-12"}
                  label="Car Rental Info"
                  value={carRentalInfo}
                  onChange={carRentalInfoHandler}
                  type="textarea"
                  rows="9"
                />
              </div>
            </div>
            <div className="col-md">
              <div className="row">
                <Col
                  col={"col-md-12"}
                  label="Hotel Price"
                  value={hotelPrice}
                  onChange={hotelPriceHandler}
                />
                <Col
                  col={"col-md-12"}
                  label="Hotel Info"
                  value={hotelInfo}
                  onChange={hotelInfoHandler}
                  type="textarea"
                  rows="9"
                />
              </div>
            </div>
          </div>
          <div className="row">
            <FileUpload
              cb={cb}
              cbref={docs}
              mode={mode}
              data={cls.docs}
              title="Docs"
            />
            <FileUpload
              cb={cb}
              cbref={adminDocs}
              mode={mode}
              data={cls.adminDocs}
              title="Admin Docs"
            />

            <Notes notes={cls.adminNotes} cb={cb} cbref={adminNotes} />
            {mode === "EDIT" && (
              <div className="col-md-4">
                <h5>Created</h5>
                <h6>{cls.created}</h6>
              </div>
            )}
          </div>
          {mode === "EDIT" && (
            <div className="accordion" id="tracks">
              <div className="accordion-item">
                <h2 className="accordion-header" id={`$heading1`}>
                  <button
                    className="accordion-button"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target={`#collapse1`}
                    aria-expanded={false}
                    aria-controls={`collapse1`}
                  >
                    <div className="row">
                      <div className="col-sm-auto">
                        <h5>{"Roster Table"}</h5>
                      </div>
                      <div className="col-sm-auto">
                        {" "}
                        {cls.type !== "Open" && cls.status === "Closed" && (
                          <Modal
                            addBtnName="Upload Roster"
                            thisModal="Upload Roster"
                            Component={RosterUploadModal}
                            props={{ clsid: cls.id }}
                          />
                        )}
                      </div>
                    </div>
                  </button>
                </h2>
                <div
                  id={`collapse1`}
                  className={`accordion-collapse collapse`}
                  aria-labelledby={`$heading1`}
                  data-bs-parent="#tracks"
                >
                  <div className="accordion-body">
                    {cls.roster && (
                      <RosterTable
                        studentss={cls.roster}
                        clsid={cls.id}
                        selectClasses={selectClasses}
                      />
                    )}
                  </div>
                </div>
              </div>
              <div className="accordion-item">
                <h2 className="accordion-header" id={`$heading2`}>
                  <button
                    className="accordion-button"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target={`#collapse2`}
                    aria-expanded={false}
                    aria-controls={`collapse2`}
                  >
                    <h5>{"Evaluations"}</h5>
                  </button>
                </h2>
                <div
                  id={`collapse2`}
                  className={`accordion-collapse collapse`}
                  aria-labelledby={`$heading2`}
                  data-bs-parent="#tracks"
                >
                  <div className="accordion-body">
                    {cls.evaluation && (
                      <Evaluations evaluations={cls.evaluation} />
                    )}
                  </div>
                </div>
              </div>
              <div className="accordion-item">
                <h2 className="accordion-header" id={`$heading3`}>
                  <button
                    className="accordion-button"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target={`#collapse3`}
                    aria-expanded={false}
                    aria-controls={`collapse3`}
                  >
                    <h5>{"AAR"}</h5>
                  </button>
                </h2>
                <div
                  id={`collapse3`}
                  className={`accordion-collapse collapse`}
                  aria-labelledby={`$heading3`}
                  data-bs-parent="#tracks"
                >
                  <div className="accordion-body">
                    {cls.aar && <AAR aar={cls.aar} />}
                  </div>
                </div>
              </div>
            </div>
          )}

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

export default ClassDetailPage;
