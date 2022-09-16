import React, { useState, useEffect, useRef } from "react";
import useHttp from "../../hooks/use-http";
import useAlert from "../../hooks/use-alert";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import TableRow from "../../util/components/TableRow";
import SetAlert from "../../util/components/SetAlert";
import { selectPromoType } from "../../constants/selectConstants";
import FilterInput from "../../util/components/FilterInput";

const PromosPage = () => {
  const [promos, setPromos] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);

  const list = ["Home", "Promos"];
  const order = [
    "id",
    "code",
    "type",
    "value",
    "singleUse",
    "expiryDate",
    "isActive",
    "created",
  ];

  useEffect(() => {
    sendRequest({ url: "/promos/" }, setPromos).catch((err) => {});
  }, [sendRequest]);

  const del = async (id) => {
    if (window.confirm(`Is it okay to delete the Promo `)) {
      try {
        await sendRequest({ method: "DELETE", url: `/promos/${id}/` }, null);
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        await sendRequest({ url: "/promos/" }, setPromos);
      } catch (error) {}
    }
  };

  const filtcol = "col-2";
  const sid = useRef({ value: "" });
  const scode = useRef({ value: "" });
  const stype = useRef({ value: "" });
  const svalue = useRef({ value: "" });
  const ssingleUse = useRef({ value: "" });
  const sexpiryDate = useRef({ value: "" });
  const sisActive = useRef({ value: "" });
  const screated = useRef({ value: "" });

  const resetFilters = (e) => {
    sid.current.value = "";
    scode.current.value = "";
    stype.current.value = "";
    svalue.current.value = "";
    ssingleUse.current.value = "";
    sexpiryDate.current.value = "";
    sisActive.current.value = "";
    screated.current.value = "";
    formref.current.reset();
  }

  const formref = useRef();

  const searchHandler = (e) => {
    if (e) e.preventDefault();
    const params = {
      sid: sid.current.value,
      scode: scode.current.value,
      stype: stype.current.value,
      svalue: svalue.current.value,
      ssingleUse: ssingleUse.current.value,
      sexpiryDate: sexpiryDate.current.value,
      sisActive: sisActive.current.value,
      screated: screated.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/promos/", params }, setPromos);
    } catch (error) {}
  };

  return (
    <div className="container-fluid p-4">
      <BreadCrumbs list={list} addEntity="promo" addBtnName="Promo" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <form onSubmit={searchHandler} ref={formref}>
        <div className="row">
          <FilterInput label="Promo Id" col={filtcol} filtref={sid} />
          <FilterInput label="Promo Code" col={filtcol} filtref={scode} />
          <FilterInput
            col={filtcol}
            val="type"
            show="type"
            label="-Type-"
            options={selectPromoType}
            filtref={stype}
          />
          <FilterInput label="Promo Value" col={filtcol} filtref={svalue} />
          <FilterInput
            col={filtcol}
            type="select"
            options={["-Single Use-", "true", "false"]}
            filtref={ssingleUse}
          />
          <FilterInput
            col={filtcol}
            type="date"
            filtref={sexpiryDate}
            label="Expiry Date"
          />
          <FilterInput
            col={filtcol}
            type="select"
            options={["-Active-", "true", "false"]}
            filtref={ssingleUse}
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
            <th scope="col">Promo Code</th>
            <th scope="col">Promo Type</th>
            <th scope="col">Promo Value</th>
            <th scope="col">Single Use</th>
            <th scope="col">Expiry Date</th>
            <th scope="col">Active</th>
            <th scope="col">Created</th>
          </tr>
        </thead>
        <tbody>
          {promos.map((promo) => (
            <TableRow
              key={promo.id}
              data={promo}
              path="promos"
              del={del}
              order={order}
            />
          ))}
         
        </tbody>
      </table>
      {promos.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Promocodes Available</h4>
            </div>
          )}
    </div>
  );
};

export default PromosPage;
