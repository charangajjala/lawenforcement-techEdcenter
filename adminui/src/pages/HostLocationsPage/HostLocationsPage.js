import React, { useState, useEffect, useRef } from "react";
import useHttp from "../../hooks/use-http";
import useAlert from "../../hooks/use-alert";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import TableRow from "../../util/components/TableRow";
import SetAlert from "../../util/components/SetAlert";
import { selectStates } from "../../constants/selectConstants";
import FilterInput from "../../util/components/FilterInput";

const HostLocationsPage = () => {
  const [locations, setLocations] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  const list = ["Home", "Locations"];
  const order = ["id", "name", "city", "state", "seats", "isActive", "created"];

  useEffect(() => {
    sendRequest({ url: "hosts/locations/" }, setLocations).catch((err) => {});
  }, [sendRequest]);

  const del = async (id) => {
    if (window.confirm(`Is it okay to delete the Location `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/hosts/locations/${id}` },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "hosts/locations/" }, setLocations);
      } catch (error) {}
    }
  };

  const filtcol = "col-2";
  const sid = useRef({ value: "" });
  const sname = useRef({ value: "" });
  const scity = useRef({ value: "" });
  const sstate = useRef({ value: "" });
  const sseats = useRef({ value: "" });
  const sactive = useRef({ value: "" });
  const screatedat = useRef({ value: "" });

  const resetFilters = (e) => {
    sid.current.value = "";
    sname.current.value = "";
    scity.current.value = "";
    sstate.current.value = "";
    sseats.current.value = "";
    sactive.current.value = "";
    screatedat.current.value = "";
    formref.current.reset();
  };

  const formref = useRef();

  const searchHandler = (e) => {
    if (e) e.preventDefault();
    const params = {
      sid: sid.current.value,
      sname: sname.current.value,
      scity: scity.current.value,
      sstate: sstate.current.value,
      sseats: sseats.current.value,
      sactive: sactive.current.value,
      screatedat: screatedat.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/hosts/locations/", params }, setLocations);
    } catch (error) {}
  };

  return (
    <div className="container-fluid p-4">
      <BreadCrumbs
        list={list}
        addEntity="hosts/location"
        addBtnName="Host Location"
      />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <FilterInput label="Host Location Id" col={filtcol} filtref={sid} />
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
            label="City"
            col={filtcol}
            filtref={sseats}
            type="number"
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
            <th scope="col">Seats</th>
            <th scope="col">Active</th>
            <th scope="col">Created</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {locations.map((location) => (
            <TableRow
              key={location.id}
              data={location}
              path="hosts/locations"
              del={del}
              order={order}
            />
          ))}
        </tbody>
      </table>
      {locations.length === 0 && (
        <div className="text-center  justify-content-center align-content-center px-5 m-5">
          <h4 className="display-4 px-5 mx-5">No Host Locations Available</h4>
        </div>
      )}
    </div>
  );
};

export default HostLocationsPage;
