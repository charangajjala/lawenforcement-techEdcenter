import React, { useState, useEffect, useRef } from "react";
import useAlert from "../../hooks/use-alert";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import TableRow from "../../util/components/TableRow";
import SetAlert from "../../util/components/SetAlert";
import useHttp from "../../hooks/use-http";
import { selectStatus } from "../../constants/selectConstants";
import FilterInput from "../../util/components/FilterInput";

const ApplicantsPage = () => {
  const [applicants, setApplicants] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const list = ["Home", "Applicants"];
  const order = ["id", "firstName", "lastName", "email", "phone", "status"];

  useEffect(() => {
    sendRequest({ url: "instructors/applicants/" }, setApplicants).catch(
      (err) => {}
    );
  }, [sendRequest]);

  const del = async (id) => {
    if (window.confirm(`Is it okay to delete the Applicant `)) {
      try {
        await sendRequest(
          {
            method: "DELETE",
            url: `instructors/applicants/${id}`,
          },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "instructors/applicants/" }, setApplicants);
      } catch (error) {}
    }
  };

  const filtcol = "col-2";
  const sid = useRef({ value: "" });
  const sfname = useRef({ value: "" });
  const slname = useRef({ value: "" });
  const semail = useRef({ value: "" });
  const sphone = useRef({ value: "" });
  const sstatus = useRef({ value: "" });

  const resetFilters = (e) => {
    sid.current.value = "";
    sfname.current.value = "";
    slname.current.value = "";
    semail.current.value = "";
    sphone.current.value = "";
    sstatus.current.value = "";
    formref.current.reset();
  };

  const formref = useRef();

  const searchHandler = (e) => {
    if (e) e.preventDefault();
    const params = {
      sid: sid.current.value,
      sfname: sfname.current.value,
      slname: slname.current.value,
      semail: semail.current.value,
      sphone: sphone.current.value,
      sactive: sstatus.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/instructors/applicants", params }, setApplicants);
    } catch (error) {}
  };

  return (
    <div className="container-fluid p-4">
      <BreadCrumbs list={list} />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <FilterInput label="Applicant Id" col={filtcol} filtref={sid} />
          <FilterInput label="First Name" col={filtcol} filtref={sfname} />
          <FilterInput label="Last Name" col={filtcol} filtref={slname} />
          <FilterInput label="Email" col={filtcol} filtref={semail} />
          <FilterInput label="Phone" col={filtcol} filtref={sphone} />
          <FilterInput
            col={filtcol}
            val="status"
            show="status"
            label="-Status-"
            options={selectStatus}
            filtref={sstatus}
          />
          <div className="col-2 m-1">
            <button type="submit" className="btn btn-primary">
              Search
            </button>
            <button
              type="button"
              className="btn btn-primary mx-3"
              onClick={resetFilters}
            >
              Reset
            </button>
          </div>
        </div>
      </form>
      <table className="table  table-striped m-2 ">
        <thead>
          <tr>
            <th scope="col">Id</th>
            <th scope="col">First Name</th>
            <th scope="col">Last Name</th>
            <th scope="col">Email</th>
            <th scope="col">Phone</th>
            <th scope="col">Status</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {applicants.map((applicant) => (
            <TableRow
              key={applicant.id}
              data={applicant}
              path="instructors/applicants"
              del={del}
              order={order}
            />
          ))}
         
        </tbody>
      </table>
      {applicants.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Applicants Available</h4>
            </div>
          )}
    </div>
  );
};

export default ApplicantsPage;
