import React, { useContext } from "react";
import logo from "../../images/logo.png";
import "./Navbar.css";
import { Link } from "react-router-dom";
import AuthContext from "../../store/auth-store";

const Navbar = () => {
  const authCtx = useContext(AuthContext);
  return (
    <nav className="navbar  bg-dark p-1">
      <div className="container-fluid">
        <Link to="/home" className="navbar-brand ">
          <img src={logo} alt="loading" />
        </Link>
        <div className="d-flex">
          <Link to="/profile">{authCtx.user.firstName}</Link>
          <button
            className="btn btn-dark"
            type="button"
            onClick={authCtx.logout}
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};
export default Navbar;
