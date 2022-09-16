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
  validateAddress,
  validateContact,
} from "../../util/helper-functions/util-functions";
import Address from "../../util/components/Address";
import Contact from "../../util/components/Contact";
import FileUpload from "../../util/components/FileUpload";
import Upload from "../../util/components/Upload";
import SelectOne from "../../util/components/SelectOne";
import SelectEntity from "../../util/components/SelectEntity";
import { selectStatus, selectHostType } from "../../constants/selectConstants";
import Modal from "../../util/components/Modal";
import HostLocationDetailPage from "../HostLocationDetailPage/HostLocationDetailPage";
import Notes from "../../util/components/Notes";

const HostDetailPage = ({ mode }) => {
  console.log("-------HostDetailPage-------");
  const [host, setHost] = useState({
    address: {},
    supervisorContact: {},
    createdBy: {},
  });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectCourses, setSelectCourses] = useState([]);
  const [selectUsers, setSelectUsers] = useState([]);
  const [selectLocations, setSelectLocations] = useState([]);

  const modalFunc = useCallback((data) => {
    setSelectLocations((prev) => {
      prev.push(data);
      return [...prev];
    });
  }, []);

  const list =
    mode === "EDIT" ? ["Home", "Hosts", `${host.name}`] : ["Home", "Hosts", ""];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest({ url: `/hosts/${params.id}` }, setHost);
        }
        await sendRequest({ url: "/courses/" }, setSelectCourses,true);
        await sendRequest({ url: "/users/" }, setSelectUsers);
        await sendRequest({ url: "/hosts/locations/" }, setSelectLocations,true);
      } catch (error) {
        //handle
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
  const [name, nameHandler] = useInput(useInputInit(host.name));
  const [website, websiteHandler] = useInput(useInputInit(host.website));
  const [comments, commentsHandler] = useInput(useInputInit(host.comments));
  const [active, activeHandler] = useInput(
    useInputInit(host.isActive),
    "checkbox"
  );

  const courses = useRef([]);
  const locations = useRef([]);
  const address = useRef({});
  const supervisorContact = useRef({});
  const docs = useRef([]);
  const contactUser = useRef("");
  const hosttype = useRef("");
  const status = useRef("");
  const logo = useRef({});
  const adminNotes = useRef([]);

  const cb = useCallback(getData, []);
  const col = "col-md-4";

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Host `)) {
      try {
        await sendRequest({ method: "DELETE", url: `/hosts/${host.id}` }, null);
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {}
    }
  };

  const submitHandler = async (e) => {
    if (e) {
      e.preventDefault();
    }
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
        website,
        supervisorContact: supervisorContact.current,
        logo: logoid,
        contactUser: parseInt(contactUser.current),
        courses: adjust(courses.current, mode),
        locations: adjust(locations.current, mode),
        hostingType: hosttype.current,
        status: status.current,
        docs: adjust(docs.current, mode),
        comments,
        adminNotes: adminNotes.current,
        isActive: active,
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
              url: `/hosts/${params.id}`,
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
  const req = !!active;
  return (
    <>
      <div className="container-fluid p-5">
        <BreadCrumbs list={list} />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="cd" onSubmit={submitHandler}>
          <div className="row">
            <Col
              col={col}
              label="Name"
              value={name}
              onChange={nameHandler}
              required={true}
            />
            <Col
              col="col-md-4"
              label="Website"
              value={website}
              onChange={websiteHandler}
              required={req}
            />
            <Upload
              title="Logo"
              cb={cb}
              cbref={logo}
              data={host.logo}
              required={req}
            />
          </div>
          <div className="row">
            <SelectOne
              col={col}
              cb={cb}
              cbref={contactUser}
              data={host.contactUser}
              selectEntitys={selectTransformUsers}
              val="id"
              show="username"
              comp="id"
              title="Contact User"
              required={req}
              initTxt="Select Contact User"
            />
            <SelectOne
              col={col}
              cb={cb}
              cbref={status}
              selectEntitys={selectStatus}
              data={host.status}
              comp="status"
              show="status"
              val="status"
              title="Status"
              required={req}
              initTxt="Select Status"
            />
            <SelectOne
              col={col}
              cb={cb}
              cbref={hosttype}
              selectEntitys={selectHostType}
              data={host.hostingType}
              comp="htype"
              show="htype"
              val="htype"
              title="Hosting Type"
              required={req}
              initTxt="Select Hosting Type"
            />
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
            <Notes notes={host.adminNotes} cb={cb} cbref={adminNotes} />
            <SelectEntity
              selectEntitys={selectCourses}
              named="title"
              data={host.courses}
              mode={mode}
              cb={cb}
              title="Courses"
              cbref={courses}
            />
            <div className="col-md-4">
              <SelectEntity
                col="col-12"
                selectEntitys={selectLocations}
                named="name"
                data={host.locations}
                mode={mode}
                cb={cb}
                title="Locations"
                cbref={locations}
                required={req}
              />
              <Modal
                Component={HostLocationDetailPage}
                modalFunc={modalFunc}
                addBtnName="Create Location"
              />
            </div>
          </div>

          <div className="row">
            <Col
              col="col-md-4"
              label="Comments"
              value={comments}
              onChange={commentsHandler}
              type="textarea"
            />
            <Col
              col={col}
              label="Active"
              value={active}
              onChange={activeHandler}
              type="checkbox"
            />
            {mode === "EDIT" && (
              <div className="row 6">
                <div className="col-md-4">
                  <h5>Created</h5>
                  <h6>{host.created}</h6>
                </div>
                <div className="col-md-4">
                  <h5>Created By</h5>
                  <h6>
                    {`${host.createdBy.firstName} ${host.createdBy.lastName}`}
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

export default HostDetailPage;
