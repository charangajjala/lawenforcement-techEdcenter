import React, { useContext } from "react";
import logo from "../../images/logo.png";
import "./Navbar.css";
import { Link } from "react-router-dom";
import AuthContext from "../../store/auth-store";

const Navbar = () => {
  const authCtx = useContext(AuthContext);

  return (
    <nav className="navbar  bg-light p-1">
      <div className="container-fluid">
        <Link to="/home" className="navbar-brand ">
          <img src={logo} alt="loading" />
        </Link>
        {authCtx.isLogin && (
          <div className="d-flex ">
            <div className="dropdown">
              <Link
                to="/userprofile"
                className="nav-link  dropdown-toggle text-dark"
                data-bs-toggle="dropdown"
                href="#"
              >
                {authCtx.user.firstName}
              </Link>
              <ul className="dropdown-menu">
                <li>
                  <Link to="/userprofile" className="dropdown-item">
                    User Profile
                  </Link>
                </li>
                {
                  /* authCtx.whichProfiles.instructor === */ authCtx.user.roles
                    .instructor && (
                    <li>
                      <Link
                        to="/instructorprofile/account"
                        className="dropdown-item"
                      >
                        Instructor Profile
                      </Link>
                    </li>
                  )
                }

                {
                  /* authCtx.whichProfiles.host === */ authCtx.user.roles.host && (
                    <li>
                      <Link to="/hostprofile/account" className="dropdown-item">
                        Host Profile
                      </Link>
                    </li>
                  )
                }
                {
                  /* authCtx.whichProfiles.student === */ authCtx.user.roles
                    .student && (
                    <li>
                      <Link
                        to="/studentprofile/account"
                        className="dropdown-item"
                      >
                        Student Profile
                      </Link>
                    </li>
                  )
                }
              </ul>
            </div>
            <button
              className="btn btn-dark"
              type="button"
              onClick={authCtx.logout}
            >
              Logout
            </button>
          </div>
        )}
        {!authCtx.isLogin && (
          <Link to="/login">
            <button className="btn btn-dark" type="button">
              Login
            </button>
          </Link>
        )}
      </div>
    </nav>
  );
};
export default Navbar;
