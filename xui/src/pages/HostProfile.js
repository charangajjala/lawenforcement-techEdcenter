import React from "react";
import HostDetailPage from "./HostDetailPage";
import HostClasses from "./components/HostClasses";
import BreadCrumbs from "../util/components/BreadCrumbs";
import { NavLink, Route, Switch } from "react-router-dom";

const HostProfile = () => {
  const list = ["Home", "Host Profile"];

  return (
    <div>
      <BreadCrumbs list={list} title="Host Profile" />
      <div className="container">
        <ul
          className="nav nav-pills mb-3 bg-white"
          id="pills-tab"
          role="tablist"
        >
          <li className="nav-item" role="presentation">
            <NavLink to="/hostprofile/account" className="nav-link">
              Account
            </NavLink>
          </li>
          <li className="nav-item" role="presentation">
            <NavLink to="/hostprofile/current" className="nav-link">
              Current Classes
            </NavLink>
          </li>
          <NavLink to="/hostprofile/past" className="nav-link">
            Past Classes
          </NavLink>
        </ul>
      </div>

      <Switch>
        <Route path="/hostprofile/account">
          <HostDetailPage mode="EDIT" />
        </Route>
        <Route path="/hostprofile/current">
          <HostClasses iscurrent={true} />
        </Route>
        <Route path="/hostprofile/past">
          <HostClasses iscurrent={false} />
        </Route>
      </Switch>
    </div>
  );
};

export default HostProfile;
