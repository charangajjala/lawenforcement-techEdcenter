import React, { useState, useEffect, useRef } from "react";
import useHttp from "../../../hooks/use-http";
import useAlert from "../../../hooks/use-alert";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import TableRow from "../../../util/components/TableRow";
import SetAlert from "../../../util/components/SetAlert";
import FilterInput from "../../../util/components/FilterInput";

const TracksPage = () => {
  const [tracks, setTracks] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage,setShowAlert);

  const list = ["Home", "Tracks"];
  const order = [
    "id",
    "title",
    "shortName",
    "numCourses",
    "isActive",
    "created",
  ];

  useEffect(() => {
    sendRequest({ url: "/courses/tracks/" }, setTracks).catch((e) => {});
  }, [sendRequest]);

  const del = async (id, ) => {
    const delTrack = tracks.find((track) => track.id === id);
    if (window.confirm(`Is it okay to delete track ${delTrack.title} `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `courses/tracks/${id}` },
          null,
          
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "/courses/tracks/" }, setTracks,);
      } catch (error) {
        
      }
    }
  };
  const filtcol = "col-2";
  const sid = useRef({ value: "" });
  const stitle = useRef({ value: "" });
  const sshtname = useRef({ value: "" });
  const sncourses = useRef({ value: "" });
  const sactive = useRef({ value: "" });
  const screatedat = useRef({ value: "" });

  const resetFilters = (e) => {
    sid.current.value = "";
    stitle.current.value = "";
    sshtname.current.value = "";
    sncourses.current.value = "";
    sactive.current.value = "";
    screatedat.current.value = "";
    formref.current.reset();
  }

  const searchHandler = (e, ) => {
    if (e) e.preventDefault();
    const params = {
      sid: sid.current.value,
      stitle: stitle.current.value,
      screatedat: screatedat.current.value,
      sshtname: sshtname.current.value,
      sactive: sactive.current.value,
      sncourses: sncourses.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest(
        { url: "/courses/tracks/", params: params },
        setTracks,
        
      );
    } catch (error) {
     
    }
  };

  const formref = useRef();

  
  return (
    <div className="container-fluid p-4">
      <BreadCrumbs list={list} addEntity="courses/track" addBtnName="Track" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <FilterInput label="Track id" col={filtcol} filtref={sid} />
          <FilterInput label="Title" col={filtcol} filtref={stitle} />
          <FilterInput label="Short Name" col={filtcol} filtref={sshtname} />
          <FilterInput
            label="No.of courses"
            col={filtcol}
            filtref={sncourses}
            type="number"
          />
          <FilterInput
            col="col-1"
            filtref={sactive}
            type="select"
            options={["-Active-", "true", "false"]}
          />
          <FilterInput col={filtcol} filtref={screatedat} type="date" />
          <div className="col-2 m-1">
            <button className="btn btn-primary" type="submit">
              Search
            </button>
            <button type="button" className="btn btn-primary mx-3" onClick={resetFilters}>
              Reset
            </button>
          </div>
        </div>
      </form>
      <table className="table  table-striped m-2 ">
        <thead>
          <tr>
            <th scope="col">Track Id</th>
            <th scope="col">Title</th>
            <th scope="col">Short Name</th>
            <th scope="col">No.of Courses</th>
            <th scope="col">Active</th>
            <th scope="col">Created</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {tracks.map((track) => (
            <TableRow
              key={track.id}
              data={track}
              path="courses/tracks"
              del={del}
              order={order}
            />
          ))}
         
        </tbody>
      </table>
      {tracks.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Tracks Available</h4>
            </div>
          )}
    </div>
  );
};

export default TracksPage;
