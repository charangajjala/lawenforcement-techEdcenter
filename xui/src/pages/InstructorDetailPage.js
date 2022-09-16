import React, { useState, useEffect, useRef, useCallback } from "react";
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
  validateAddress,
  validateContact,
} from "../util/helper-functions/util-functions";
import Address from "../util/components/Address";
import Contact from "../util/components/Contact";
import FileUpload from "../util/components/FileUpload";
import Upload from "../util/components/Upload";

const InstructorDetailPage = ({ mode }) => {
  console.log("-----InstructorDetailPage-------");
  const [instructor, setInstructor] = useState({
    agencyAddress: {},
    agencyContact: {},
    emergencyContact: {},
  });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest({ url: `/instructors/` }, setInstructor);
        }
      } catch (error) {
        //handle error
      }
    };

    fetch();
  }, [mode, sendRequest, params.id]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [dob, dobHandler] = useInput(useInputInit(instructor.dob));
  const [ssn, ssnHandler] = useInput(useInputInit(instructor.ssn));
  const [bio, bioHandler] = useInput(useInputInit(instructor.bio));
  const [agencyName, agencyNameHandler] = useInput(
    useInputInit(instructor.agencyName)
  );

  const [retiredDate, retiredDateHandler] = useInput(
    useInputInit(instructor.retiredDate)
  );
  const [closestAirports, closestAirportsHandler] = useInput(
    useInputInit(instructor.closestAirports)
  );
  const [preferredAirports, preferredAirportsHandler] = useInput(
    useInputInit(instructor.preferredAirports)
  );
  const [travelNotes, travelNotesHandler] = useInput(
    useInputInit(instructor.travelNotes)
  );

  const agencyAddress = useRef({});
  const agencyContact = useRef({});
  const emergencyContact = useRef({});
  const docs = useRef([]);

  const image = useRef({});

  const cb = useCallback(getData, []);
  const col = "col-md-4";

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Instructor`)) {
      try {
        await sendRequest(
          {
            method: "DELETE",
            url: `/instructors/`,
          },
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
      validateAddress(agencyAddress.current, setAlertMessage, setShowAlert);
      validateContact(agencyContact.current, setAlertMessage, setShowAlert);
      validateContact(emergencyContact.current, setAlertMessage, setShowAlert);
      let imageId;

      if (image && image.current.name)
        await fileRequest(
          { url: "/file/", method: "POST", body: image.current },
          (id) => {
            imageId = id.id;
          },
          null
        );

      const setDocId = (doc, id) => {
        doc.id = id.id;
      };

      for (const doc of docs.current) {
        if (doc.old !== true && doc.action === "ADD" && doc) {
          await fileRequest(
            { url: "/file/", method: "POST", body: doc.file },
            setDocId.bind(null, doc),
            doc.name
          );
        }
      }

      const newInstructor = {
        image: imageId, //adjust later
        dob,
        ssn,
        bio,
        agencyName,
        agencyAddress: agencyAddress.current,
        agencyContact: { ...agencyContact.current },
        emergencyContact: { ...emergencyContact.current },
        docs: adjust(docs.current),

        retiredDate,
        closestAirports,
        preferredAirports,
        travelNotes,
      };
      console.log("old", newInstructor);
      checkAddEmpty(newInstructor);
      if (mode === "EDIT") {
        checkIfEdited(newInstructor, instructor);
      }

      console.log("new ", newInstructor);
      if (Object.keys(newInstructor).length !== 0) {
        if (mode === "ADD") {
          await sendRequest(
            {
              method: "POST",
              url: "/instructors/",
              body: newInstructor,
            },
            null
          );
        }
        if (mode === "EDIT") {
          await sendRequest(
            {
              method: "PUT",
              url: `/instructors/`,
              body: newInstructor,
            },
            null
          );
        }
        console.log("<<<<<sent req in submit handler>>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (e) {}
  };
  return (
    <>
      <div className="container">
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="" onSubmit={submitHandler}>
          <div className="row">
            <div className="col-md-8">
              <div className="row">
                <Col
                  col="col-md-6"
                  label="Date Of Birth"
                  type="date"
                  value={dob}
                  onChange={dobHandler}
                  required={true}
                />
                <Col
                  col="col-md-6"
                  label="SSN"
                  value={ssn}
                  onChange={ssnHandler}
                  required={true}
                />
                <Col
                  col="col-md-6"
                  label="Agency Name"
                  value={agencyName}
                  onChange={agencyNameHandler}
                  required={true}
                />
                <Col
                  col="col-md-6"
                  label="Retired Date"
                  value={retiredDate}
                  onChange={retiredDateHandler}
                  type="date"
                />
                <Upload
                  col="col-md-6"
                  title="Image"
                  cb={cb}
                  cbref={image}
                  data={instructor.image}
                />
              </div>
            </div>

            <div className="col-md-4">
              <Col
                label="Bio"
                value={bio}
                onChange={bioHandler}
                type="textarea"
                rows={/* instructor.image?"19":"12" */ "18"}
                required={true}
              />
            </div>
          </div>
          <div className="row ">
            <div className="row ">
              <div className="col-md-4">
                <h5>Agency Address</h5>
                <Address
                  init={instructor.agencyAddress}
                  cb={cb}
                  cbref={agencyAddress}
                  mode={mode}
                />
              </div>
              <div className="col-md-4">
                <h5>Agency Contact</h5>
                <Contact
                  init={instructor.agencyContact}
                  cb={cb}
                  cbref={agencyContact}
                  mode={mode}
                />
              </div>
              <div className="col-md-4">
                <h5>Emergency Contact</h5>
                <Contact
                  init={instructor.emergencyContact}
                  cb={cb}
                  cbref={emergencyContact}
                  mode={mode}
                />
              </div>
            </div>
            <div className="row ">
              <Col
                col={col}
                label="Closest Airports"
                value={closestAirports}
                onChange={closestAirportsHandler}
                type="textarea"
              />
              <Col
                col={col}
                label="Preferred Airports"
                value={preferredAirports}
                onChange={preferredAirportsHandler}
                type="textarea"
              />
              <Col
                col={col}
                label="Travel Notes"
                value={travelNotes}
                onChange={travelNotesHandler}
                type="textarea"
              />
            </div>
            <div className="row ">
              <FileUpload
                cb={cb}
                cbref={docs}
                mode={mode}
                data={instructor.docs}
                title="Docs"
              />
            </div>
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

export default InstructorDetailPage;
