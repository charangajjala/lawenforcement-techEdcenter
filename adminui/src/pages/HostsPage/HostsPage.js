import React, { useState, useEffect, useRef } from "react";
import useAlert from "../../hooks/use-alert";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import TableRow from "../../util/components/TableRow";
import SetAlert from "../../util/components/SetAlert";
import useHttp from "../../hooks/use-http";
import { selectStatus, selectStates } from "../../constants/selectConstants";
import FilterInput from "../../util/components/FilterInput";

const HostsPage = () => {
  const [hosts, setHosts] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  const list = ["Home", "Hosts"];
  const order = [
    "id",
    "name",
    "city",
    "state",
    "status",
    "isActive",
    "created",
  ];

  useEffect(() => {
    sendRequest({ url: "/hosts/" }, setHosts).catch((err) => {});
  }, [sendRequest]);

  const del = async (id) => {
    if (window.confirm(`Is it okay to delete the Host `)) {
      try {
        await sendRequest({ method: "DELETE", url: `hosts/${id}` }, null);
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "/hosts/" }, setHosts);
      } catch (error) {}
    }
  };

  const filtcol = "col-2";
  const sid = useRef({ value: "" });
  const sname = useRef({ value: "" });
  const scity = useRef({ value: "" });
  const sstate = useRef({ value: "" });
  const sstatus = useRef({ value: "" });
  const sactive = useRef({ value: "" });
  const screatedat = useRef({ value: "" });

  const resetFilters = (e) => {
    sid.current.value = "";
    sname.current.value = "";
    scity.current.value = "";
    sstate.current.value = "";
    sstatus.current.value = "";
    sactive.current.value = "";
    screatedat.current.value = "";
    formref.current.reset();
  }

  const formref = useRef();

  const searchHandler = async (e) => {
    if (e) e.preventDefault();
    const params = {
      sid: sid.current.value,
      sname: sname.current.value,
      scity: scity.current.value,
      sstate: sstate.current.value,
      sstatus: sstatus.current.value,
      sactive: sactive.current.value,
      screatedat: screatedat.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      await sendRequest({ url: "/hosts/", params }, setHosts);
    } catch (error) {}
  };

  return (
    <div className="container-fluid p-4">
      <BreadCrumbs list={list} addEntity="host" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <FilterInput label="Host Id" col={filtcol} filtref={sid} />
          <FilterInput label="Name" col={filtcol} filtref={sname} />
          <FilterInput label="City" col={filtcol} filtref={scity} />
          <FilterInput
            col={filtcol}
            val="value"
            show="name"
            label="-State-"
            options={selectStates}
            filtref={sstate}
          />
          <FilterInput
            col={filtcol}
            val="status"
            show="status"
            label="-Status-"
            options={selectStatus}
            filtref={sstatus}
          />
          <FilterInput
            col={filtcol}
            type="select"
            options={["-Active-", "true", "false"]}
            filtref={sactive}
          />
          <FilterInput col={filtcol} type="date" filtref={screatedat} />
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
            <th scope="col">Name</th>
            <th scope="col">City</th>
            <th scope="col">State</th>
            <th scope="col">Status</th>
            <th scope="col">Active</th>
            <th scope="col">Created</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {hosts.map((applicant) => (
            <TableRow
              key={applicant.id}
              data={applicant}
              path="hosts"
              del={del}
              order={order}
            />
          ))}
         
        </tbody>
      </table>
      {hosts.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Hosts Available</h4>
            </div>
          )}
    </div>
  );
};

export default HostsPage;
