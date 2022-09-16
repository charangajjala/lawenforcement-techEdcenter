import React, { useEffect, useState, useRef, useCallback } from "react";
import useInput from "../../../hooks/use-input";
import useHttp from "../../../hooks/use-http";
import { useParams } from "react-router-dom";
import useAlert from "../../../hooks/use-alert";
import Col from "../../../util/components/Col";
import SelectEntity from "../../../util/components/SelectEntity";
import Desc from "../../../util/components/Desc";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import SetAlert from "../../../util/components/SetAlert";
import {
  giveTransformDesc,
  adjust,
  checkAddEmpty,
  checkIfEdited,
  getData,
} from "../../../util/helper-functions/util-functions";
import Upload from "../../../util/components/Upload";

const TrackDetailPage = ({ mode }) => {
  const [track, setTrack] = useState({ createdBy: {} });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectCourses, setSelectCourses] = useState([]);

  const list =
    mode === "EDIT"
      ? [
          { name: "Home", path: "/home" },
          { name: "Tracks", path: "/courses/tracks" },
          `${track.title} `,
        ]
      : [
          { name: "Home", path: "/home" },
          { name: "tracks", path: "/courses/tracks" },
          "",
        ];

  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    async function fetch() {
      try {
        if (mode === "EDIT")
          await sendRequest({ url: `courses/tracks/${params.id}` }, setTrack);
        await sendRequest({ url: `/courses/` }, setSelectCourses,true);
      } catch (error) {
        //handle error
      }
    }
    fetch();
  }, [mode, params.id, sendRequest]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);

  const [title, titleHandler] = useInput(useInputInit(track.title));
  const [sname, snameHandler] = useInput(useInputInit(track.shortName));
  const [what, whatHandler] = useInput(useInputInit(track.what));
  const [why, whyHandler] = useInput(useInputInit(track.why));
  const [how, howHandler] = useInput(useInputInit(track.how));
  const [maintainance, maintainanceHandler] = useInput(
    useInputInit(track.maintainance)
  );
  const [ncourses, ncoursesHandler] = useInput(useInputInit(track.numCourses));
  const [active, activeHandler] = useInput(
    useInputInit(track.isActive),
    "checkbox"
  );

  const whoObj = useRef({});
  const requirementsObj = useRef({});
  const benefitsObj = useRef({});
  const requiredCourses = useRef([]);
  const optionalCourses = useRef([]);

  const logo = useRef({});

  const del = async () => {
    const delTrack = track;
    if (window.confirm(`Is it okay to delete track ${delTrack.title} `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/tracks/${track.id}` },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {}
    }
  };
  const cb = useCallback(getData, []);

  const submitHandler = async (e) => {
    if (e) e.preventDefault();
    let logoid;
    try {
      if (logo.current.name)
        await fileRequest(
          {
            url: "/file/",
            method: "POST",
            body: logo.current,
            headers: { "Content-Type": "multipart/form-data" },
          },
          (id) => {
            logoid = id.id;
          },
          null
        );

      const newTrack = {
        title,
        shortName: sname,
        what,
        why,
        how,
        maintainance,
        numCourses: parseInt(ncourses),
        isActive: active,
        who: giveTransformDesc(whoObj.current),
        benefits: giveTransformDesc(benefitsObj.current),
        requirements: giveTransformDesc(requirementsObj.current),
        requiredCourses: adjust(requiredCourses.current, mode),
        optionalCourses: adjust(optionalCourses.current, mode),
        logo: logoid,
      };
      console.log("old", newTrack);
      checkAddEmpty(newTrack);
      if (mode === "EDIT") checkIfEdited(newTrack, track);
      console.log("new", newTrack);

      if (Object.keys(newTrack).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            {
              method: "POST",
              url: "/courses/tracks/",
              body: newTrack,
            },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/courses/tracks/${params.id}`,
              body: newTrack,
            },
            null
          );
        console.log("<<<<sent req in submit>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };
  const req = !!active;
  return (
    <div className="container-fluid p-5">
      <BreadCrumbs list={list} mode={true} />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form className="cd " onSubmit={submitHandler}>
        <div className="row 1">
          <Upload
            title="Logo"
            cb={cb}
            cbref={logo}
            data={track.logo}
            col="col-md-3"
            required={req}
          />
          <div className="col">
            <div className="row">
              <Col
                col="col-md-4"
                label="Title"
                value={title}
                onChange={titleHandler}
                required={true}
              />
              <Col
                col="col-md-4"
                label="Short Name"
                value={sname}
                onChange={snameHandler}
                required={req}
              />
              <Col
                col="col-md-3"
                label="No.of Courses"
                value={ncourses}
                onChange={ncoursesHandler}
                type="num"
                required={req}
              />
              <Col
                col="col-md"
                label="Active"
                value={active}
                onChange={activeHandler}
                type="checkbox"
              />
              <Col
                col="col-md-4 "
                label="What"
                value={what}
                onChange={whatHandler}
                type="textarea"
                rows="5"
                required={req}
              />
              <Col
                col="col-md-4 "
                label="Why"
                value={why}
                onChange={whyHandler}
                type="textarea"
                rows="5"
                required={req}
              />
              <Col
                col="col-md-4 "
                label="How"
                value={how}
                onChange={howHandler}
                type="textarea"
                rows="5"
                required={req}
              />
            </div>
          </div>
        </div>
        <div className="row ">
          <Desc
            title="Who"
            descData={track.who}
            cb={cb}
            cbref={whoObj}
            required={req}
          />
          <Desc
            title="Benifits"
            descData={track.benefits}
            cb={cb}
            cbref={benefitsObj}
            required={req}
          />
          <Desc
            title="Requirements"
            descData={track.requirements}
            cb={cb}
            cbref={requirementsObj}
            required={req}
          />
        </div>
        <div className="row">
          <SelectEntity
            title="Required Courses"
            selectEntitys={selectCourses}
            named="title"
            data={track.requiredCourses}
            cb={cb}
            mode={mode}
            cbref={requiredCourses}
            required={req}
          />
          <SelectEntity
            title="Optional Courses"
            data={track.optionalCourses}
            selectEntitys={selectCourses}
            named="title"
            cb={cb}
            mode={mode}
            cbref={optionalCourses}
            required={req}
          />
          <Col
            col="col-md-4"
            label="Maintainance"
            value={maintainance}
            onChange={maintainanceHandler}
            required={req}
          />
          {mode === "EDIT" && (
            <div className="col-md-4">
              <h5>Created</h5>
              <h6>{track.created}</h6>
            </div>
          )}
          {mode === "EDIT" && (
            <div className="col-md-4">
              <h5>Created By</h5>
              <h6>
                {`${track.createdBy.firstName} ${track.createdBy.lastName}`}
              </h6>
            </div>
          )}
        </div>

        <button type="submit" className="btn btn-primary">
          Save
        </button>
        {mode === "EDIT" && (
          <button className="btn btn-danger mx-5" type="button" onClick={del}>
            Delete track
          </button>
        )}
      </form>
    </div>
  );
};

export default TrackDetailPage;
