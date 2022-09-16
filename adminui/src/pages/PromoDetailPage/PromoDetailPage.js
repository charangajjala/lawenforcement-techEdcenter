import React, { useState, useEffect, useRef, useCallback } from "react";
import useInput from "../../hooks/use-input";
import useHttp from "../../hooks/use-http";
import { useParams } from "react-router-dom";
import Col from "../../util/components/Col";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import {
  checkAddEmpty,
  checkIfEdited,
  getData,
} from "../../util/helper-functions/util-functions";
import SelectOne from "../../util/components/SelectOne";
import { selectPromoType } from "../../constants/selectConstants";

const PromoDetailPage = ({ mode }) => {
  console.log("-------PromoDetailPage-------");
  const [promo, setPromo] = useState({});
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();

  const list =
    mode === "EDIT"
      ? ["Home", "promos", `${promo.code}`]
      : ["Home", "promos", ""];

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest({ url: `/promos/${params.id}/` }, setPromo);
        }
      } catch (error) {
        //handle
      }
    };
    fetch();
  }, [mode, params.id, sendRequest]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [code, codeHandler] = useInput(useInputInit(promo.code));
  const [value, valueHandler] = useInput(useInputInit(promo.value));
  const [expiryDate, expiryDateHandler] = useInput(
    useInputInit(promo.expiryDate)
  );
  const [active, activeHandler] = useInput(
    useInputInit(promo.isActive),
    "checkbox"
  );
  const [singleUse, singleUseHandler] = useInput(
    useInputInit(promo.singleUse),
    "checkbox"
  );

  const promotype = useRef("");

  const cb = useCallback(getData, []);

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Promo `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/promos/${promo.id}/` },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
      } catch (error) {}
    }
  };

  const submitHandler = async (e) => {
    if (e) {
      e.preventDefault();
    }
    try {
      const newpromo = {
        code,
        value,
        expiryDate,
        singleUse,
        type: promotype.current,
        isActive: active,
      };
      console.log("old", newpromo);
      checkAddEmpty(newpromo);
      if (mode === "EDIT") {
        checkIfEdited(newpromo, promo);
      }
      console.log("new ", newpromo);
      if (Object.keys(newpromo).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            { method: "POST", url: "/promos/", body: newpromo },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/promos/${params.id}/`,
              body: newpromo,
            },
            null
          );
        console.log("<<<<sent req in submit>>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };
  //const req= !!active;
  return (
    <>
      <div className="container-fluid p-5">
        <BreadCrumbs list={list} />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="cd" onSubmit={submitHandler}>
          <div className="row">
            <Col
              col={"col-md-4"}
              label="Promo Code"
              value={code}
              onChange={codeHandler}
              required={true}
            />
            <SelectOne
              col={"col-md-4"}
              cb={cb}
              cbref={promotype}
              selectEntitys={selectPromoType}
              data={promo.type}
              comp="type"
              show="type"
              val="type"
              title="Promo Type"
              initTxt="-Select Promo Type-"
            />
            <Col
              col={"col-md"}
              label="Active"
              value={active}
              onChange={activeHandler}
              type="checkbox"
            />
            <Col
              col={"col-md"}
              label="Single Use"
              value={singleUse}
              onChange={singleUseHandler}
              type="checkbox"
            />
          </div>
          <div className="row">
            <Col
              col="col-md-4"
              label="Promo Value"
              value={value}
              onChange={valueHandler}
            />
            <Col
              col="col-md-4"
              label="Expiry Date"
              value={expiryDate}
              onChange={expiryDateHandler}
              type="date"
            />

            {mode === "EDIT" && (
              <div className="row 6">
                <div className="col-md-4">
                  <h5>Created</h5>
                  <h6>{promo.created}</h6>
                </div>
              </div>
            )}
          </div>

          <button type="submit" className="btn btn-primary">
            Save
          </button>
          {mode === "EDIT" && (
            <button className="btn btn-danger mx-5" type="button" onClick={del}>
              Delete promo
            </button>
          )}
        </form>
      </div>
    </>
  );
};

export default PromoDetailPage;
