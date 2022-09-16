import React, { useCallback, useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import useInput from "../../../hooks/use-input";
import useAlert from "../../../hooks/use-alert";
import useHttp from "../../../hooks/use-http";
import Col from "../../../util/components/Col";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import SetAlert from "../../../util/components/SetAlert";
import Address from "../../../util/components/Address";
import {
  getData,
  checkIfEdited,
  checkAddEmpty,
  validateAddress,
} from "../../../util/helper-functions/util-functions";

const UserDetailPage = ({ mode }) => {
  console.log("-------UserDetailPage-------");
  const [user, setUser] = useState({ createdBy: {}, address: {} });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const list =
    mode === "EDIT"
      ? ["Home", "Users", `${user.firstName} ${user.lastName}`]
      : ["Home", "Users", ""];

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    if (mode === "EDIT") {
      sendRequest({ url: `/users/${params.id}/` }, setUser).catch(() => {});
    }
  }, [mode, sendRequest, params.id]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);

  const [fName, fNameHandler] = useInput(useInputInit(user.firstName));
  const [lName, lNameHandler] = useInput(useInputInit(user.lastName));
  const [title, titleHandler] = useInput(useInputInit(user.title));
  const [email, emailHandler] = useInput(useInputInit(user.email));
  const [email2, email2Handler] = useInput(useInputInit(user.email2));
  const [phone, phoneHandler] = useInput(useInputInit(user.phone));
  const [phone2, phone2Handler] = useInput(useInputInit(user.phone2));
  const [password, passwordHandler] = useInput(useInputInit(user.password));
  const [isAdmin, isAdminHandler] = useInput(
    useInputInit(user.isAdmin),
    "checkbox"
  );
  const [isSuperUser, isSuperUserHandler] = useInput(
    useInputInit(user.isSuperUser),
    "checkbox"
  );
  const address = useRef({});

  const cb = useCallback(getData, []);
  const col = "col-12 p-0";

  const del = async () => {
    const delUser = user;
    if (
      window.confirm(
        `Is it okay to delete user ${delUser.firstName} ${delUser.lastName}`
      )
    ) {
      try {
        await sendRequest({ method: "DELETE", url: `/users/${user.id}` }, null);
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: `/users/${params.id}/` }, setUser).catch(() => {});
      } catch (error) {}
    }
  };

  const submitHandler = async (e) => {
    if (e) e.preventDefault();

    try {
      validateAddress(address.current, setAlertMessage, setShowAlert);

      const newUser = {
        firstName: fName,
        lastName: lName,
        title,
        email,
        email2,
        phone2,
        phone,
        password,
        isAdmin,
        isSuperUser,
        address: address.current,
      };
      console.log("old", newUser);
      checkAddEmpty(newUser);
      if (mode === "EDIT") {
        checkIfEdited(newUser, user);
      }
      console.log("new", newUser);

      if (Object.keys(newUser).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            { method: "POST", url: "/users/", body: newUser },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/users/${user.id}/`,
              body: newUser,
            },
            null
          );
        console.log("<<<<<<<<<<sent req in submit>>>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (e) {}
  };

  

  return (
    <div className="container-fluid px-5 py-3">
      <BreadCrumbs list={list} />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form className="cd " onSubmit={submitHandler}>
        <div className="row p-0">
          <div className="col-2"></div>
          <div className="col-md-4">
            <div className="row">
              <Col
                col={col}
                label="First Name"
                value={fName}
                onChange={fNameHandler}
                required={true}
              />
              <Col
                col={col}
                label="Last Name"
                value={lName}
                onChange={lNameHandler}
                required = {true}
              />
              <Col
                col={col}
                label="Title"
                value={title}
                onChange={titleHandler}
              />
              <Col
                col={col}
                label="Email"
                value={email}
                onChange={emailHandler}
                type="email"
                required={true}
              />

              <Col
                col={col}
                label="Password"
                value={password}
                onChange={passwordHandler}
                type="password"
              />
              <Col
                col={col}
                label="Phone"
                value={phone}
                onChange={phoneHandler}
              />
              <Col
                col={col}
                label="Alternate Email"
                value={email2}
                onChange={email2Handler}
                type="email"
                required={false}
              />
              <Col
                col={col}
                label="Alternate Phone"
                value={phone2}
                onChange={phone2Handler}
                required={false}
              />
            </div>
          </div>
          <div className="col-md-4">
            <Address init={user.address} cb={cb} cbref={address} mode={mode} />
            <div className="row p-0">
              <div className="col-2"></div>
              <Col
                col="col-4 p-0"
                label="Admin"
                value={isAdmin}
                onChange={isAdminHandler}
                type="checkbox"
              />
              <Col
                col="col-5 p-0"
                label="Super User"
                value={isSuperUser}
                onChange={isSuperUserHandler}
                type="checkbox"
              />
              <div className="col-1 "></div>
              <div className="col-2"></div>
              {mode === "EDIT" && (
                <div className="col-4 p-0 mt-4">
                  <h5>Created</h5>
                  <p>{user.created}</p>
                </div>
              )}
              {mode === "EDIT" &&
                !!user.createdBy &&
                !!user.createdBy.firstName && (
                  <div className="col-4 p-0 mt-4">
                    <h5>Created By</h5>
                    <h6>
                      {`${user.createdBy.firstName} ${user.createdBy.lastName}`}
                    </h6>
                  </div>
                )}
              <div className="col-2"></div>
            </div>
          </div>
        </div>

        <button type="submit" className="btn btn-primary">
          Save
        </button>
        {mode === "EDIT" && (
          <button className="btn btn-danger mx-5" type="button" onClick={del}>
            Delete User
          </button>
        )}
      </form>
    </div>
  );
};

export default UserDetailPage;
