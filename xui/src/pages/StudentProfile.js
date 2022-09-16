import React from "react";
import StudentDetailPage from "./StudentDetailPage";
import StudentCurrentClasses from "./components/StudentCurrentClasses";
import StudentPastClasses from "./components/StudentPastClasses";
import StudentTracks from "./components/StudentTracks";
import BreadCrumbs from "../util/components/BreadCrumbs";
import { NavLink, Route, Switch } from "react-router-dom";

const StudentProfile = () => {
  const list = ["Home", "Student Profile"];

  return (
    <div>
      <BreadCrumbs list={list} title="Student Profile" />
      <div className="container">
        <ul
          className="nav nav-pills mb-3 bg-white"
          id="pills-tab"
          role="tablist"
        >
          <li className="nav-item" role="presentation">
            <NavLink to="/studentprofile/account" className="nav-link">
              Account
            </NavLink>
          </li>
          <li className="nav-item" role="presentation">
            <NavLink to="/studentprofile/current" className="nav-link">
              Current Classes
            </NavLink>
          </li>
          <NavLink to="/studentprofile/past" className="nav-link">
            Past Classes
          </NavLink>
          <li className="nav-item" role="presentation">
            <NavLink to="/studentprofile/tracks" className="nav-link">
              Tracks
            </NavLink>
          </li>
        </ul>
      </div>

      <Switch>
        <Route path="/studentprofile/account">
          <StudentDetailPage mode="EDIT" />
        </Route>
        <Route path="/studentprofile/current">
          <StudentCurrentClasses />
        </Route>
        <Route path="/studentprofile/past">
          <StudentPastClasses />
        </Route>
        <Route path="/studentprofile/tracks">
          <StudentTracks />
        </Route>
      </Switch>
    </div>
  );
};

export default StudentProfile;
