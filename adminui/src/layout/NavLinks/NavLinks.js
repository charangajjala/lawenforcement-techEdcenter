import React from "react";
import "./NavLinks.css";
import { NavLink } from "react-router-dom";

const NavLinks = () => {
  return (
    <div className="container-fluid">
      <ul className="nav  bg-light ">
        <li className="nav-item font-weight-bold  ">
          <NavLink to="/courses" exact className="nav-link  ">
            <h6>Courses</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/users" className="nav-link ">
            <h6>Users</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/courses/topics" className="nav-link ">
            <h6>Topics</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/courses/tracks" className="nav-link ">
            <h6>Tracks</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink exact to="/instructors" className="nav-link ">
            <h6>Instructors</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/instructors/applicants" className="nav-link ">
            <h6>Applicants</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink exact to="/hosts" className="nav-link ">
            <h6>Hosts</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/hosts/locations" className="nav-link ">
            <h6>Host Locations</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/students" className="nav-link ">
            <h6>Students</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/classes" className="nav-link ">
            <h6>Classes</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/invoices" className="nav-link ">
            <h6>Invoices</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/promos" className="nav-link ">
            <h6>Promos</h6>
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink to="/hours" className="nav-link ">
            <h6>Hours</h6>
          </NavLink>
        </li>
      </ul>
    </div>
  );
};

export default NavLinks;
