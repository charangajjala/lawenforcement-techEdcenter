import React, { useState, useEffect, useRef, useCallback } from "react";

//import axios from "../util/axios";
import useInput from "../hooks/use-input";

import useHttp from "../hooks/use-http";
import Col from "../util/components/Col";
import {
  getData,
  checkIfEdited,
  checkAddEmpty,
  validateAddress,
  validateContact,
} from "../util/helper-functions/util-functions";
import BreadCrumbs from "../util/components/BreadCrumbs";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";
import Address from "../util/components/Address";
import Contact from "../util/components/Contact";

const HostLocationDetailPage = ({ mode, isModal, modalFunc, id }) => {
  const [location, setLocation] = useState({
    address: {},
    locationContact: {},
  });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
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

  useEffect(() => {
    if (mode === "EDIT") {
      sendRequest({ url: `hosts/locations/` }, setLocation).catch((err) => {});
    }
  }, [mode, sendRequest]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [name, nameHandler] = useInput(useInputInit(location.name));
  const [seats, seatsHandler] = useInput(useInputInit(location.seats));
  const [closestAirports, closestAirportsHandler] = useInput(
    useInputInit(location.closestAirports)
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
  const locationContact = useRef({});

  const cb = useCallback(getData, []);
  const col = "col-md-4";

  const del = async () => {
    if (window.confirm(`Is it okay to delete the location `)) {
      try {
        await sendRequest({ method: "DELETE", url: `/locations/` }, null);
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
      validateAddress(address.current.value, setAlertMessage, setShowAlert);
      validateContact(
        locationContact.current.value,
        setAlertMessage,
        setShowAlert
      );

      const newLocation = {
        name,
        seats,
        
        isAudioEnabled,
        isWifiEnabled,
        isProjectionEnabled,
        isMicAvailable,
        hasFlatScreens,
        address: address.current,
        locationContact: locationContact.current,
        closestAirports,
        
        
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
              url: `/hosts/locations/`,
              body: newLocation,
            },
            modalFunc
          );
        console.log("<<<sent req in submit>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };
  return (
    <>
      <div className="container-fluid p-5">
        {/* isModal && <BreadCrumbs list={list} mode={true} /> */}
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="cd " onSubmit={submitHandler}>
          <div className="row">
            <Col
              col={col}
              label="Name"
              value={name}
              onChange={nameHandler}
              type="textarea"
              required={true}
            />
            <Col
              col="col-md-6"
              label="Seats"
              type="number"
              value={seats}
              onChange={seatsHandler}
            />

            <div className="col-md-4">
              <h5>Agency Address</h5>
              <Address
                init={location.address}
                cb={cb}
                cbref={address}
                mode={mode}
              />
            </div>
            <div className="col-md-4">
              <h5>Location Contact</h5>
              <Contact
                init={location.locationContact}
                cb={cb}
                cbref={locationContact}
                mode={mode}
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

              <Col
                col={col}
                label="Wifi Enabled"
                value={isWifiEnabled}
                onChange={isWifiEnabledHandler}
                type="checkbox"
                required={true}
              />
              <Col
                col={col}
                label="Audio Enabled"
                value={isAudioEnabled}
                onChange={isAudioEnabledHandler}
                type="checkbox"
                required={true}
              />
              <Col
                col={col}
                label="Projection Enabled"
                value={isProjectionEnabled}
                onChange={isProjectionEnabledHandler}
                type="checkbox"
                required={true}
              />
              <Col
                col={col}
                label="Mic Available"
                value={isMicAvailable}
                onChange={isMicAvailableHandler}
                type="checkbox"
                required={true}
              />
              <Col
                col={col}
                label="Flat Screens"
                value={hasFlatScreens}
                onChange={hasFlatScreensHandler}
                type="checkbox"
                required={true}
              />
            </div>
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
