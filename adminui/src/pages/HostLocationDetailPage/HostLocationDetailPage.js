import React, { useState, useEffect, useRef, useCallback } from "react";
import useInput from "../../hooks/use-input";
import useHttp from "../../hooks/use-http";
import { useParams } from "react-router-dom";
import Col from "../../util/components/Col";
import {
  getData,
  checkIfEdited,
  checkAddEmpty,
  validateAddress,
  validateContact,
} from "../../util/helper-functions/util-functions";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import Address from "../../util/components/Address";
import Contact from "../../util/components/Contact";
import Notes from "../../util/components/Notes";

const HostLocationDetailPage = ({ mode, isModal, modalFunc }) => {
  const [location, setLocation] = useState({
    address: {},
    locationContact: {},
    createdBy: {},
  });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const list =
    mode === "EDIT"
      ? [
          { name: "Home", path: "/home" },
          { name: "Host Locations", path: "/hosts/locations" },
          { name: `${location.name} ` },
        ]
      : [
          { name: "Home", path: "/home" },
          { name: "Host Locations", path: "/hosts/locations" },
          "",
        ];

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    if (mode === "EDIT") {
      sendRequest({ url: `hosts/locations/${params.id}` }, setLocation).catch(
        (err) => {}
      );
    }
  }, [mode, params.id, sendRequest]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [name, nameHandler] = useInput(useInputInit(location.name));
  const [seats, seatsHandler] = useInput(useInputInit(location.seats));
  const [closestAirports, closestAirportsHandler] = useInput(
    useInputInit(location.closestAirports)
  );

  const [active, activeHandler] = useInput(
    useInputInit(location.isActive),
    "checkbox"
  );
  const [isWifiEnabled, isWifiEnabledHandler] = useInput(
    useInputInit(location.isWifiEnabled),
    "checkbox"
  );
  const [isAudioEnabled, isAudioEnabledHandler] = useInput(
    useInputInit(location.isAudioEnabled),
    "checkbox"
  );
  const [isProjectionEnabled, isProjectionEnabledHandler] = useInput(
    useInputInit(location.isProjectionEnabled),
    "checkbox"
  );
  const [isMicAvailable, isMicAvailableHandler] = useInput(
    useInputInit(location.isMicAvailable),
    "checkbox"
  );
  const [hasFlatScreens, hasFlatScreensHandler] = useInput(
    useInputInit(location.hasFlatScreens),
    "checkbox"
  );

  const [notes, notesHandler] = useInput(useInputInit(location.notes));

  const address = useRef({});
  const intel = useRef({});
  const locationContact = useRef({});
  const adminNotes = useRef([]);
  const cb = useCallback(getData, []);
  const col = "col-md-4";

  const del = async () => {
    if (window.confirm(`Is it okay to delete the location `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/locations/${params.id}` },
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
      e.stopPropagation();
    }
    try {
      validateAddress(address.current, setAlertMessage, setShowAlert);
      validateContact(locationContact.current, setAlertMessage, setShowAlert);

      const newLocation = {
        name,
        seats,
        isActive: active,
        isAudioEnabled,
        isWifiEnabled,
        isProjectionEnabled,
        isMicAvailable,
        hasFlatScreens,
        address: address.current,
        locationContact: locationContact.current,
        closestAirports,
        intel: intel.current,
        adminNotes: adminNotes.current,
        notes,
      };
      console.log("old", newLocation);
      checkAddEmpty(newLocation);
      if (mode === "EDIT") {
        checkIfEdited(newLocation, location);
      }
      console.log("new ", newLocation);

      if (Object.keys(newLocation).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            {
              method: "POST",
              url: "/hosts/locations/",
              body: newLocation,
            },
            modalFunc
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/hosts/locations/${params.id}`,
              body: newLocation,
            },
            null
          );
        console.log("<<<sent req in submit>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };
  const req = !!active;
  return (
    <>
      <div className="container-fluid p-5">
        {!isModal && <BreadCrumbs list={list} mode={true} />}
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="cd " onSubmit={submitHandler}>
          <div className="row">
            <Col
              col={"col-md-4"}
              label="Location Name"
              value={name}
              onChange={nameHandler}
              required={true}
            />
            <Col
              col="col-md-2"
              label="Seats"
              type="number"
              value={seats}
              onChange={seatsHandler}
              required={req}
            />
            <div className="col-md-6">
              {" "}
              <div className="row">
                <Col
                  col={"col-md-4"}
                  label="Active"
                  value={active}
                  onChange={activeHandler}
                  type="checkbox"
                />
                <Col
                  col={"col-md-4"}
                  label="Wifi Enabled"
                  value={isWifiEnabled}
                  onChange={isWifiEnabledHandler}
                  type="checkbox"
                  required={req}
                />
                <Col
                  col={"col-md-4"}
                  label="Audio Enabled"
                  value={isAudioEnabled}
                  onChange={isAudioEnabledHandler}
                  type="checkbox"
                  required={req}
                />
                <Col
                  col={"col-md-4"}
                  label="Projection Enabled"
                  value={isProjectionEnabled}
                  onChange={isProjectionEnabledHandler}
                  type="checkbox"
                  required={req}
                />
                <Col
                  col={"col-md-4"}
                  label="Mic Available"
                  value={isMicAvailable}
                  onChange={isMicAvailableHandler}
                  type="checkbox"
                  required={req}
                />
                <Col
                  col={"col-md-4"}
                  label="Flat Screens"
                  value={hasFlatScreens}
                  onChange={hasFlatScreensHandler}
                  type="checkbox"
                  required={req}
                />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-4">
              <h6 className="p-0 m-0">Agency Address</h6>
              <Address
                init={location.address}
                cb={cb}
                cbref={address}
                mode={mode}
              />
            </div>
            <div className="col-md-4">
              <h6 className="p-0 m-0">Location Contact</h6>
              <Contact
                init={location.locationContact}
                cb={cb}
                cbref={locationContact}
                mode={mode}
              />
            </div>
            <Notes
              notes={location.adminNotes}
              cb={cb}
              cbref={adminNotes}
              maxheight="600px"
            />
            <Notes
              notes={location.intel}
              cb={cb}
              cbref={intel}
              title="Intel"
              maxheight="600px"
            />
            <Col
              col={col}
              label="Closest Airports"
              value={closestAirports}
              onChange={closestAirportsHandler}
              type="textarea"
            />

            <Col
              col={col}
              label="Notes"
              value={notes}
              onChange={notesHandler}
              type="textarea"
            />
          </div>
          <div className="row">
            {mode === "EDIT" && (
              <div className="row 6">
                <div className="col-md-4">
                  <h6>Created</h6>
                  <h6>{location.created}</h6>
                </div>
                <div className="col-md-4">
                  <h6>Created By</h6>
                  <h6>
                    {`${location.createdBy.firstName} ${location.createdBy.lastName}`}
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
              Delete Host Location
            </button>
          )}
        </form>
      </div>
    </>
  );
};

export default HostLocationDetailPage;
