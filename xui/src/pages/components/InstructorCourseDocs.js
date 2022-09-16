import React, { useState, useEffect } from "react";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import Modal from "../../util/components/Modal";
import DocPage from "./DocModalPage";

const InstructorCourseDocs = () => {
  const [courses, setCourses] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  useEffect(() => {
    sendRequest({ url: "/classes/instructor/courseDocs/" }, setCourses).catch(
      (_) => {}
    );
  }, [sendRequest]);

  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <table class="table table-borderless table-striped table-sm">
        <tr class="border bg-primary text-white">
          <th>Course Id</th>
          <th>Course Title</th>
          <th>Action</th>
          <th></th>
        </tr>
        <tbody>
          {courses.map((course) => (
            <tr key={course.courseId}>
              <td>{course.courseId}</td>
              <td>{course.title}</td>
              <td>
                <Modal
                  Component={DocPage}
                  mdltitle="View/Edit"
                  props={{
                    url: `classes/instructor/courseDocs/`,
                    params: { courseId: course.courseId },
                    initdocs: course.docs,
                  }}
                  thisModal="View/Edit"
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InstructorCourseDocs;
