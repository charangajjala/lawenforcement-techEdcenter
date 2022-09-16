import React, { useRef, useContext, useState } from "react";
import "./Login.css";
import AuthContext from "../store/auth-store";
import { axiosDefault } from "../util/axios";
import BreadCrumbs from "../util/components/BreadCrumbs";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";

const Login = () => {
  const emailRef = useRef();
  const passRef = useRef();
  const [showPass, setShowPass] = useState(false);
  const authCtx = useContext(AuthContext);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const list = ["Home", "Login"];
  const submitHandler = async (e) => {
    e.preventDefault();
    //backend request...
    console.log(emailRef.current.value, passRef.current.value);
    const email = emailRef.current.value;
    const password = passRef.current.value;
    try {
      const res = await axiosDefault.post("/authentication/", {
        email,
        password,
      });
      authCtx.login(res.data.access, res.data.refresh, res.data.user);
    } catch (e) {
      //handle error
      setShowAlert(true);
      if (e.response && e.response.status === 401) {
        /*  const alertMessage = [].concat.apply(
          [],
          addBuffer(Object.values(e.response.data))
        ); */
        setAlertMessage({
          e: true,
          message: "Invalid Credentials",
        });
      } else {
        setAlertMessage({
          e: true,
          message: "An Error has occurred",
        });
      }
    }
  };

  return (
    <div className="">
      <BreadCrumbs list={list} title="Login" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form
        id="loginForm"
        onSubmit={submitHandler}
        className="mt-5 text-center"
      >
        <input
          type="text  "
          className="form-control-lg mb-1 form-control-1"
          placeholder="Email"
          required
          ref={emailRef}
        />
        <input
          type={showPass ? "text" : "password"}
          placeholder="Password"
          className="form-control-lg form-control-1"
          required
          ref={passRef}
        />
        <label htmlFor="show">Show Password</label>
        <input
          id="show"
          type="checkbox"
          checked={showPass}
          className="form-check-input "
          onChange={(e) => {
            setShowPass(e.target.checked);
          }}
        />
        <div className="text-center mt-3">
          <button type="submit" className="btn btn-lg btn-primary btn-block">
            Sign In
          </button>
        </div>
        <div className="lostP">
          <a href="/login">lost Password</a>
        </div>
      </form>
    </div>
  );
};

export default Login;
