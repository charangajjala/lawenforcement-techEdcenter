import React from "react";
import { NavLink } from "react-router-dom";
import "./NavLinks.css";

const NavLinks = () => {
  return (
    <div className="navbar ">
      <div className="container-fluid px-4">
        <ul className="nav ">
          <li className="nav-item ">
            <NavLink to="/classes" className="nav-link text-white">
              <h6 className="p-0 m-0">Training Schedule</h6>
            </NavLink>
          </li>
          <li className="nav-item dropdown m-auto p-auto">
            <a className="nav-link text-white" href="#">
              <h6 className="p-0 m-0">Training</h6>
            </a>
            <div className="dropdown-menu bg-light">
              <NavLink to="/classes" className="  dropdown-item">
                <h6 className="p-0 m-0">Training Schedule</h6>
              </NavLink>
              <NavLink to="/courses" exact className=" dropdown-item ">
                <h6 className="p-0 m-0">Courses</h6>
              </NavLink>
              <NavLink to="/courses/tracks" className=" dropdown-item ">
                <h6 className="p-0 m-0">Certification Tracks</h6>
              </NavLink>
              <a class="dropdown-item" href="{% url 'evaluations' %}">
                Evaluations
              </a>
              <NavLink to="/hostprofileadd" className=" dropdown-item">
                <h6 className="p-0 m-0"> Become Host</h6>
              </NavLink>
              <NavLink to="/Gsa" className=" dropdown-item">
                <h6 className="p-0 m-0">Gsa</h6>
              </NavLink>
            </div>
          </li>
          <li className="nav-item dropdown m-auto p-auto  ">
            <a className="nav-link text-white" href="#">
              <h6 className="p-0 m-0">About</h6>
            </a>
            <div className="dropdown-menu bg-light">
              <NavLink to="/MissionStatement" className=" dropdown-item">
                <h6 className="p-0 m-0">Mission Statement</h6>
              </NavLink>
              <NavLink to="/History" className=" dropdown-item">
                <h6 className="p-0 m-0">History</h6>
              </NavLink>
              <NavLink to="/instructors" className=" dropdown-item">
                <h6 className="p-0 m-0">Team</h6>
              </NavLink>
              <NavLink to="/Careers" className=" dropdown-item">
                <h6 className="p-0 m-0">Careers</h6>
              </NavLink>
              <NavLink to="/CompanyDoc" className=" dropdown-item">
                <h6 className="p-0 m-0">Company Documentation</h6>
              </NavLink>
              <NavLink to="/Faq" className=" dropdown-item">
                <h6 className="p-0 m-0">Faq</h6>
              </NavLink>
            </div>
          </li>
          <li className="nav-item">
            <NavLink to="/applicantprofileadd" className="nav-link text-white">
              <h6 className="p-0 m-0">Instructor Applicant</h6>
            </NavLink>
          </li>

          <li className="nav-item">
            <NavLink to="/Contact" className="nav-link text-white">
              <h6 className="p-0 m-0">Contact</h6>
            </NavLink>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default NavLinks;
