import React, { useContext } from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import Navbar from "./layout/Navbar/Navbar";
import NavLinks from "./layout/NavLinks/NavLinks";
import Home from "./pages/home";
import CoursesPage from "./pages/CoursesPage";
import InstructorsPage from "./pages/InstructorsPage";
import CourseDetailPage from "./pages/CourseDetailPage";
import TracksPage from "./pages/TracksPage";
import UserProfilePage from "./pages/UserProfilePage";
import ApplicantDetailPage from "./pages/ApplicantDetailPage";
import HostDetailPage from "./pages/HostDetailPage";
import HostLocationDetailPage from "./pages/HostLocationDetailPage";
import Login from "./pages/Login";
import AuthContext from "../src/store/auth-store";
import ClassesPage from "./pages/ClassesPage";
import ClassDetailPage from "./pages/ClassDetailPage";
import ClassRegisterPage from "./pages/ClassRegisterPage";
import StudentProfile from "./pages/StudentProfile";
import InstructorProfile from "./pages/InstructorProfile";
import HostProfile from "./pages/HostProfile";
import InvoicePage, { OldInvoice } from "./pages/InvoicePage";
import SetAlert from "./util/components/SetAlert";
import useAlert from "./hooks/use-alert";
import Careers from "./pages/StaticPages/Careers";
import CompanyDoc from "./pages/StaticPages/CompanyDoc";
import Contact from "./pages/StaticPages/Contact";
import Faq from "./pages/StaticPages/Faq";
import Gsa from "./pages/StaticPages/Gsa";
import History from "./pages/StaticPages/History";
import MissionStatement from "./pages/StaticPages/MissionStatement";

function App() {
  console.log("<<<App.js>>>");
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const authCtx = useContext(AuthContext);

  /* useEffect(() => {
    if (authCtx.isLogin && !authCtx.whichProfiles.stop) {
      authCtx.getProfiles(sendRequest);
    }
  }, [authCtx, sendRequest]); */

  return (
    <div style={{ overflowX: "hidden", overflowY: "hidden" }}>
      <Navbar />
      <NavLinks />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <Switch>
        {!authCtx.isLogin && (
          <Route exact path="/login">
            <Login />
          </Route>
        )}
        <Route path="/home">
          <Home />
        </Route>
        <Route exact path="/courses">
          <CoursesPage />
        </Route>
        <Route exact path="/courses/tracks">
          <TracksPage />
        </Route>
        <Route path="/courses/:id">
          <CourseDetailPage />
        </Route>
        <Route path="/instructors">
          <InstructorsPage />
        </Route>
        <Route path="/hostprofileadd">
          <HostDetailPage mode="ADD" />
        </Route>
        <Route exact path="/classes">
          <ClassesPage />
        </Route>
        <Route path="/classes/register/:id">
          <ClassRegisterPage />
        </Route>
        <Route path="/classes/:id">
          <ClassDetailPage />
        </Route>
        <Route exact path="/invoice/:invoiceNum/:accessKey">
          <InvoicePage />
        </Route>
        <Route path="/invoice">
          <OldInvoice />
        </Route>
        <Route path="/Careers">
          <Careers />
        </Route>
        <Route path="/CompanyDoc">
          <CompanyDoc />
        </Route>
        <Route path="/Contact">
          <Contact />
        </Route>
        <Route path="/Faq">
          <Faq />
        </Route>
        <Route path="/Gsa">
          <Gsa />
        </Route>
        <Route path="/History">
          <History />
        </Route>
        <Route path="/MissionStatement">
          <MissionStatement />
        </Route>
        {authCtx.isLogin && (
          <>
            <Route path="/login">
              <Redirect to="/home" />
            </Route>
            <Route path="/userprofile">
              <UserProfilePage mode="EDIT" />
            </Route>
            <Route path="/instructorprofile">
              <InstructorProfile mode="EDIT" />
            </Route>
            <Route path="/applicantprofileadd">
              <ApplicantDetailPage mode="ADD" />
            </Route>
            <Route path="/hostprofile">
              <HostProfile mode="EDIT" />
            </Route>
            <Route exact path="/locationprofile">
              <HostLocationDetailPage mode="EDIT" />
            </Route>
            <Route path="/locationprofileadd">
              <HostLocationDetailPage mode="ADD" />
            </Route>
            <Route path="/studentprofile">
              <StudentProfile mode="EDIT" />
            </Route>
            <Route path="/">
              <Redirect to="/home" />
            </Route>
          </>
        )}
        <Route path="/">
          <Redirect to="/home" />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
