import React, { useContext } from "react";
import Login from "./pages/LoginPage/Login";
import HomePage from "./pages/HomePage/Homepage";
import CoursePage from "./pages/Courses/CoursePage/CoursePage";
import UsersPage from "./pages/Users/UsersPage/UsersPage";
import Navbar from "./layout/Navbar/Navbar";
import NavLinks from "./layout/NavLinks/NavLinks";
import CourseDetailPage from "./pages/Courses/CourseDetailPage/CourseDetailPage";
import TopicPage from "./pages/Topics/TopicPage/TopicPage";
import { Route, Switch, Redirect } from "react-router-dom";
import UserDetailPage from "./pages/Users/UserDetailPage/UserDetailPage";
import AuthContext from "./store/auth-store";
import TopicDetailPage from "./pages/Topics/TopicDetailPage/TopicDetailPage";
import TracksPage from "./pages/Tracks/TrackPage/TrackPage";
import TrackDetailPage from "./pages/Tracks/TrackDetailPage/TrackDetailPage";
import InstructorsPage from "./pages/InstructorsPage/InstructorsPage";
import InstructorDetailPage from "./pages/InstructorDetailPage/InstructorDetailPage";
import ApplicantsPage from "./pages/ApplicantsPage/ApplicantsPage";
import ApplicantDetailPage from "./pages/ApplicantDetailPage/ApplicantDetailPage";
import HostsPage from "./pages/HostsPage/HostsPage";
import HostDetailPage from "./pages/HostDetailPage/HostDetailPage";
import HostLocationsPage from "./pages/HostLocationsPage/HostLocationsPage";
import HostLocationDetailPage from "./pages/HostLocationDetailPage/HostLocationDetailPage";
import StudentsPage from "./pages/StudentsPage/StudentsPage";
import StudentDetailPage from "./pages/StudentDetailPage/StudentDetailPage";
import ClassesPage from "./pages/ClassesPage/ClassesPage";
import ClassDetailPage from "./pages/ClassDetailPage/ClassDetailPage";
import InvoicesPage from "./pages/InvoicesPage/InvoicesPage";
import InvoiceDetailPage from "./pages/InvoiceDetailPage/InvoiceDetailPage";
import PromosPage from "./pages/PromosPage/PromosPage";
import PromoDetailPage from "./pages/PromoDetailPage/PromoDetailPage";
import Hours from "./pages/Hours/Hours";
import Error from "./util/components/Error";

//import axios from "./util/axios";

function App() {
  console.log("-----App.js-------");
const authCtx = useContext(AuthContext);

  return (
    <Switch>
      {authCtx.error.set && (
        <Route path="/">
          <Error err={authCtx.error.data} />
        </Route>
      )}
      <Route path="/">
        <>
          {!authCtx.isLogin && (
            <>
              <Route to="/login">
                <Login />
              </Route>
              <Route path="/">
                <Redirect to="/login" />
              </Route>
            </>
          )}
          {authCtx.isLogin && (
            <>
              <>
                <Navbar logoutUser={authCtx.logout} />
                <NavLinks />
              </>
              <Switch>
                <Route exact path="/login">
                  <Redirect to="/home" />
                </Route>
                <Route path="/home">
                  <HomePage />
                </Route>
                <Route exact path="/courses">
                  <CoursePage />
                </Route>
                <Route path="/course">
                  <CourseDetailPage mode="ADD" />
                </Route>
                <Route exact path="/courses/topics">
                  <TopicPage />
                </Route>
                <Route path="/courses/topic">
                  <TopicDetailPage mode="ADD" />
                </Route>
                <Route path="/courses/topics/:id">
                  <TopicDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/courses/tracks">
                  <TracksPage />
                </Route>
                <Route path="/courses/track">
                  <TrackDetailPage mode="ADD" />
                </Route>
                <Route path="/courses/tracks/:id">
                  <TrackDetailPage mode="EDIT" />
                </Route>
                <Route path="/courses/:id">
                  <CourseDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/users">
                  <UsersPage />
                </Route>
                <Route path="/user">
                  <UserDetailPage mode="ADD" />
                </Route>
                <Route path="/users/:id">
                  <UserDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/instructors">
                  <InstructorsPage />
                </Route>
                <Route exact path="/instructors/applicants">
                  <ApplicantsPage />
                </Route>
                <Route path="/instructors/applicants/:id">
                  <ApplicantDetailPage mode="EDIT" />
                </Route>
                <Route path="/instructor">
                  <InstructorDetailPage mode="ADD" />
                </Route>
                <Route path="/instructors/:id">
                  <InstructorDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/hosts">
                  <HostsPage />
                </Route>
                <Route exact path="/hosts/locations">
                  <HostLocationsPage />
                </Route>
                <Route path="/hosts/location">
                  <HostLocationDetailPage mode="ADD" />
                </Route>
                <Route path="/hosts/locations/:id">
                  <HostLocationDetailPage mode="EDIT" />
                </Route>
                <Route path="/host">
                  <HostDetailPage mode="ADD" />
                </Route>
                <Route path="/hosts/:id">
                  <HostDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/students">
                  <StudentsPage />
                </Route>
                <Route path="/student">
                  <StudentDetailPage mode="ADD" />
                </Route>
                <Route path="/students/:id">
                  <StudentDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/classes">
                  <ClassesPage />
                </Route>
                <Route path="/cls">
                  <ClassDetailPage mode="ADD" />
                </Route>
                <Route path="/classes/:id">
                  <ClassDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/invoices">
                  <InvoicesPage />
                </Route>
                <Route exact path="/invoice">
                  <InvoiceDetailPage mode="ADD" />
                </Route>
                <Route path="/invoices/:invoiceNum">
                  <InvoiceDetailPage mode="EDIT" />
                </Route>
                <Route exact path="/promos">
                  <PromosPage />
                </Route>
                <Route path="/promo">
                  <PromoDetailPage mode="ADD" />
                </Route>
                <Route path="/promos/:id">
                  <PromoDetailPage mode="EDIT" />
                </Route>
                <Route path="/hours">
                  <Hours />
                </Route>
                <Route path="/">
                  <HomePage />
                </Route>
              </Switch>
            </>
          )}
        </>
      </Route>
    </Switch>
  );
}

export default App;
