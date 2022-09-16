import React from "react";
import InstructorDetailPage from "./InstructorDetailPage";
import InstructorCurrentClasses from "./components/InstructorCurrentClasses";
import InstructorPastClasses from "./components/InstructorPastClasses";
import BreadCrumbs from "../util/components/BreadCrumbs";
import InstructorCourseDocs from "./components/InstructorCourseDocs";
import { NavLink, Route, Switch } from "react-router-dom";

const InstructorProfile = () => {
  const list = ["Home", "Profile"];

  return (
    <div>
      <BreadCrumbs list={list} title="Instructor Profile" />
      <div className="container">
        <ul
          className="nav nav-pills mb-3 bg-white"
          id="pills-tab"
          role="tablist"
        >
          <li className="nav-item" role="presentation">
            <NavLink to="/instructorprofile/account" className="nav-link">
              Account
            </NavLink>
          </li>
          <li className="nav-item" role="presentation">
            <NavLink to="/instructorprofile/current" className="nav-link">
              Current Classes
            </NavLink>
          </li>
          <NavLink to="/instructorprofile/past" className="nav-link">
            Past Classes
          </NavLink>
          <li className="nav-item" role="presentation">
            <NavLink to="/instructorprofile/tracks" className="nav-link">
              Course Materials
            </NavLink>
          </li>
        </ul>
      </div>
      <Switch>
        <Route path="/instructorprofile/account">
          <InstructorDetailPage mode="EDIT" />
        </Route>
        <Route path="/instructorprofile/current">
          <InstructorCurrentClasses />
        </Route>
        <Route path="/instructorprofile/past">
          <InstructorPastClasses />
        </Route>
        <Route path="/instructorprofile/tracks">
          <InstructorCourseDocs />
        </Route>
      </Switch>
    </div>
  );
};

export default InstructorProfile;
