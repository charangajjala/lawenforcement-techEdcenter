import React, { useState, useEffect, useRef, useCallback } from "react";

//import axios from "../util/axios";
import useInput from "../hooks/use-input";

import useHttp from "../hooks/use-http";

import Col from "../util/components/Col";
import BreadCrumbs from "../util/components/BreadCrumbs";
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
import SelectOne from "../util/components/SelectOne";
import SelectEntity from "../util/components/SelectEntity";
import { selectStatus, selectHostType } from "../constants/selectConstants";
import HostLocationDetailPage from "./HostLocationDetailPage";
import Modal from "../util/components/Modal";

const HostDetailPage = ({ mode }) => {
  const [host, setHost] = useState({
    address: {},
    supervisorContact: {},
  });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectCourses, setSelectCourses] = useState([]);

  const [selectLocations, setSelectLocations] = useState([]);

  const modalFunc = useCallback((data) => {
    setSelectLocations((prevLocs) => {
      const existingLoc = prevLocs.find((loc) => loc.id === data.id);
      if (existingLoc) existingLoc.name = data.name;
      else prevLocs.push(data);
      return [...prevLocs];
    });
  }, []);

  const list = ["Home", "Become a Host"];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest({ url: `/hosts/` }, setHost);
        }
        await sendRequest({ url: "/courses/" }, setSelectCourses);

        await sendRequest({ url: "/hosts/locations/" }, setSelectLocations);
      } catch (error) {
        //handle
      }
    };
    fetch();
  }, [mode, sendRequest]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [name, nameHandler] = useInput(useInputInit(host.name));
  const [website, websiteHandler] = useInput(useInputInit(host.website));
  const [comments, commentsHandler] = useInput(useInputInit(host.comments));

  const courses = useRef([]);
  const locations = useRef([]);
  const address = useRef({});
  const supervisorContact = useRef({});
  const docs = useRef([]);
  const contactuserid = useRef("");
  const hosttype = useRef("");
  const logo = useRef();

  const cb = useCallback(getData, []);

  const submitHandler = async (e) => {
    if (e) e.preventDefault();
    try {
      validateAddress(address.current, setAlertMessage, setShowAlert);
      validateContact(supervisorContact.current, setAlertMessage, setShowAlert);

      let logoid;

      if (logo.current.name) {
        await fileRequest(
          { url: "/file/", method: "POST", body: logo.current },
          (id) => {
            logoid = id.id;
          },
          null
        );
      }

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

      const newHost = {
        name,
        address: address.current,
        supervisorContact: supervisorContact.current,
        logo: logoid,
        contactUserId: parseInt(contactuserid.current),
        courses: adjust(courses.current),
        locations: adjust(locations.current),
        hostingType: hosttype.current,
        docs: adjust(docs.current),
        comments,
      };
      console.log("old", newHost);
      checkAddEmpty(newHost);
      if (mode === "EDIT") {
        checkIfEdited(newHost, host);
      }
      console.log("new ", newHost);
      if (Object.keys(newHost).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            { method: "POST", url: "/hosts/", body: newHost },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/hosts/`,
              body: newHost,
            },
            null
          );
        console.log("<<<<sent req in submit>>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };
  return (
    <div>
      {mode === "ADD" && <BreadCrumbs list={list} title="Become a Host" />}
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <div className="container">
        <form className="cd" onSubmit={submitHandler}>
          <div className="row">
            <div className="col">
              <div className="row">
                <Col
                  col={"col-md-6"}
                  label="Name"
                  value={name}
                  onChange={nameHandler}
                  required={true}
                />
                <Col
                  col="col-md-6"
                  label="Website"
                  value={website}
                  onChange={websiteHandler}
                  required={true}
                />

                <SelectOne
                  col={"col-md-6"}
                  cb={cb}
                  cbref={hosttype}
                  selectEntitys={selectHostType}
                  data={host.hostingType}
                  comp="htype"
                  show="htype"
                  val="htype"
                  title="Hosting Type"
                  required={true}
                  initTxt="Select Hosting Type"
                />
                {host.logo && (
                  <Col
                    col="col-md"
                    label="Comments"
                    value={comments}
                    onChange={commentsHandler}
                    type="textarea"
                  />
                )}
              </div>
            </div>

            <Upload title="Logo" cb={cb} cbref={logo} data={host.logo} />
          </div>
          <div className="row ">
            <div className="col-md-4">
              <h6 className="p-0 m-0"> Address</h6>
              <Address
                init={host.address}
                cb={cb}
                cbref={address}
                mode={mode}
              />
            </div>
            <div className="col-md-4">
              <h6 className="p-0 m-0">Supervisor Contact</h6>
              <Contact
                init={host.supervisorContact}
                cb={cb}
                cbref={supervisorContact}
                mode={mode}
              />
            </div>
            <FileUpload
              cb={cb}
              cbref={docs}
              mode={mode}
              data={host.docs}
              title="Docs"
              maxheight="600px"
            />
          </div>

          <div className="row">
            <SelectEntity
              selectEntitys={selectCourses}
              named="title"
              data={host.courses}
              mode={mode}
              cb={cb}
              title="Courses"
              cbref={courses}
              required={true}
            />
            <div className="col-md-4">
              <SelectEntity
                selectEntitys={selectLocations}
                named="name"
                data={host.locations}
                mode={mode}
                cb={cb}
                col="col-12"
                title="Locations"
                cbref={locations}
                modalFunc={modalFunc}
                isModal={true}
                ModalComp={HostLocationDetailPage}
                mdltitle="Edit Location"
                required={true}
              />
              <Modal
                props={{ mode: "ADD", modalFunc: modalFunc }}
                Component={HostLocationDetailPage}
                mdltitle="Create Location"
              />
            </div>
            {!host.logo && (
              <Col
                col="col-md-4"
                label="Comments"
                value={comments}
                onChange={commentsHandler}
                type="textarea"
              />
            )}
          </div>

          <button type="submit" className="btn btn-primary">
            Save
          </button>
        </form>
      </div>
    </div>
  );
};

export default HostDetailPage;
