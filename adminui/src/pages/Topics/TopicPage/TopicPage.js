import React, { useState, useEffect, useRef } from "react";
import useAlert from "../../../hooks/use-alert";
import useHttp from "../../../hooks/use-http";
import BreadCrumbs from "../../../util/components/BreadCrumbs";
import TableRow from "../../../util/components/TableRow";
import SetAlert from "../../../util/components/SetAlert";
import FilterInput from "../../../util/components/FilterInput";

const TopicPage = () => {
  const [topics, setTopics] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  const list = ["Home", "Topics"];
  const order = ["id", "name", "created"];

  useEffect(() => {
    sendRequest({ url: "/courses/topics/" }, setTopics).catch((e) => {});
  }, [sendRequest]);

  const del = async (id) => {
    const delTopic = topics.find((topic) => topic.id === id);
    if (window.confirm(`Is it okay to delete topic ${delTopic.name} `)) {
      try {
        await sendRequest(
          {
            method: "DELETE",
            url: `/courses/topics/${id}/`,
          },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "/courses/topics/" }, setTopics);
      } catch (error) {}
    }
  };

  const stid = useRef({ value: "" });
  const stname = useRef({ value: "" });
  const screatedat = useRef({ value: "" });
  const filtcol = "col-2";

  const resetFilters = (e) => {
    stid.current.value = "";
    stname.current.value = "";
    screatedat.current.value = "";
    formref.current.reset();
  }

  const formref = useRef();

  const searchHandler = (e) => {
    if (e) e.preventDefault();
    const params = {
      stid: stid.current.value,
      stname: stname.current.value,
      screatedat: screatedat.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/courses/topics/", params: params }, setTopics);
    } catch (error) {}
  };

  return (
    <div className="container-fluid p-4">
      <BreadCrumbs list={list} addEntity="courses/topic" addBtnName="TOPIC" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <FilterInput col={filtcol} label="Topic Id" filtref={stid} />
          <FilterInput col={filtcol} label="Topic Name" filtref={stname} />
          <FilterInput col={filtcol} filtref={screatedat} type="date" />
          <div className="col-2 m-1">
            <button className="btn btn-primary" type="submit">
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
            <th scope="col">Topic Id</th>
            <th scope="col">Name</th>
            <th scope="col">Created</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {topics.map((topic) => (
            <TableRow
              key={topic.id}
              data={topic}
              path="courses/topics"
              del={del}
              order={order}
            />
          ))}
         
        </tbody>
      </table>
      {topics.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Topics Available</h4>
            </div>
          )}
    </div>
  );
};

export default TopicPage;
