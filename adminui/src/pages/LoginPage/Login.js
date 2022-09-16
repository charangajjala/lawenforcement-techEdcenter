import React, { useRef, useContext, useState } from "react";
import "./Login.css";
import logo from "../../images/logo.png";
import AuthContext from "../../store/auth-store";
import { axiosDefault } from "../../util/axios";
import useAlert from "../../hooks/use-alert";
import SetAlert from "../../util/components/SetAlert";

const Login = () => {
  const emailRef = useRef();
  const passRef = useRef();
  const [showPass, setShowPass] = useState(false);
  const authCtx = useContext(AuthContext);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const submitHandler = async (e) => {
    e.preventDefault();
    //backend request...
    console.log(emailRef.current.value, passRef.current.value);
    const email = emailRef.current.value;
    const password = passRef.current.value;
    try {
      const res = await axiosDefault.post("admin/authentication/", {
        email,
        password,
      });
      authCtx.login(res.data.access, res.data.refresh, res.data.user);
      //authCtx.login("a", "r");
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
    <div className="text-center mt-5">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form id="loginForm" onSubmit={submitHandler}>
        <img className="mt-4 img-fluid" src={logo} alt="Loading" />
        <input
          type="email" //email
          className=" form-control-lg form-control-1 mb-1 "
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
          className="form-check-input mx-2"
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
