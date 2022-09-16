import React, { useState, useEffect, useRef } from "react";
import useHttp from "../../../hooks/use-http";
import useAlert from "../../../hooks/use-alert";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import TableRow from "../../../util/components/TableRow";
import SetAlert from "../../../util/components/SetAlert";
import FilterInput from "../../../util/components/FilterInput";

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp();

  const list = ["Home", "Users"];

  const order = [
    "id",
    "firstName",
    "lastName",
    "email",
    "phone",
    "isAdmin",
    "isSuperUser",
  ];

  useEffect(() => {
    sendRequest({ url: "/users/" }, setUsers).catch((e) => {});
  }, [sendRequest]);

  const del = async (id) => {
    const delUser = users.find((user) => user.id === id);
    if (
      window.confirm(
        `Is it okay to delete user ${delUser.firstName} ${delUser.lastName}`
      )
    ) {
      try {
        await sendRequest({ method: "DELETE", url: `/users/${id}/` }, null);
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "/users/" }, setUsers);
      } catch (error) {}
    }
  };
  const filtcol = "col-auto";
  const sid = useRef({ value: "" });
  const sfname = useRef({ value: "" });
  const slname = useRef({ value: "" });
  const semail = useRef({ value: "" });
  const sphone = useRef({ value: "" });
  const sadmin = useRef({ value: "" });
  const sspuser = useRef({ value: "" });

  const resetFilters = (e) => {
    sid.current.value = "";
    sfname.current.value = "";
    slname.current.value = "";
    semail.current.value = "";
    sphone.current.value = "";
    sadmin.current.value = "";
    sspuser.current.value = "";
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
      sadmin: sadmin.current.value,
      sspuser: sspuser.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/users/", params: params }, setUsers);
    } catch (error) {}
  };
  return (
    <>
      <div className="container-fluid p-4">
        <BreadCrumbs list={list} addEntity="user" />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form onSubmit={searchHandler} ref={formref}>
          <div className="row">
            <FilterInput label="User Id" filtref={sid} col={filtcol} />
            <FilterInput label="First Name" filtref={sfname} col={filtcol} />
            <FilterInput label="Last Name" filtref={slname} col={filtcol} />
            <FilterInput label="Email" filtref={semail} col={filtcol} />
            <FilterInput label="Phone" filtref={sphone} col={filtcol} />
            <FilterInput
              filtref={sadmin}
              col={filtcol}
              type="select"
              options={["-Admin-", "true", "false"]}
            />
            <FilterInput
              filtref={sspuser}
              col={filtcol}
              type="select"
              options={["-Super User-", "true", "false"]}
            />
            <div className="col-sm m-1">
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
        <table className="table  table-striped ">
          <thead>
            <tr>
              <th scope="col"> Id</th>
              <th scope="col">First Name</th>
              <th scope="col">Last Name</th>
              <th scope="col">Email</th>
              <th scope="col">Phone</th>
              <th scope="col">Admin</th>
              <th scope="col">Super User</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <TableRow
                key={user.id}
                data={user}
                path="users"
                del={del}
                order={order}
              />
            ))}
          </tbody>
        </table>
        {users.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Users Available</h4>
            </div>
          )}
      </div>
    </>
  );
};

export default UsersPage;
