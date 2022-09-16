import React, { useState, useEffect, useRef, useCallback } from "react";
import useInput from "../../hooks/use-input";
import useHttp from "../../hooks/use-http";
import { useParams } from "react-router-dom";
import Col from "../../util/components/Col";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import {
  adjust,
  checkAddEmpty,
  checkIfEdited,
  getData,
  validateAddress,
  validateContact,
} from "../../util/helper-functions/util-functions";
import Address from "../../util/components/Address";
import Contact from "../../util/components/Contact";
import SelectOne from "../../util/components/SelectOne";
import SelectEntity from "../../util/components/SelectEntity";
import { selectInvoiceType } from "../../constants/selectConstants";

const InvoiceDetailPage = ({ mode }) => {
  console.log("-------InvoiceDetailPage-------");
  const [invoice, setInvoice] = useState({
    pmrAddress: {},
    pmrContact: {},
    createdBy: {},
  });
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [selectClasses, setSelectClasses] = useState([]);
  const [selectStudents, setSelectStudents] = useState([]);
  const [selectPromos, setSelectPromos] = useState([]);
  const list =
    mode === "EDIT"
      ? ["Home", "invoices", `${invoice.invoiceNum}`]
      : ["Home", "invoices", ""];

  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const params = useParams();

  useEffect(() => {
    const fetch = async () => {
      try {
        if (mode === "EDIT") {
          await sendRequest(
            { url: `/invoice/${params.invoiceNum}` },
            setInvoice
          );
        }
        await sendRequest({ url: "/classes/" }, setSelectClasses);
        await sendRequest({ url: "/students/" }, setSelectStudents, true);
        await sendRequest(
          { url: "/promos/", params: { options: true } },
          setSelectPromos,
          true
        );
      } catch (error) {
        //handle
      }
    };
    fetch();
  }, [mode, params, sendRequest]);

  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [pmrAgency, pmrAgencyHandler] = useInput(
    useInputInit(invoice.pmrAgency)
  );
  const [paymentMethod, paymentMethodHandler] = useInput(
    useInputInit(invoice.paymentMethod)
  );
  const [paidDate, paidDateHandler] = useInput(useInputInit(invoice.paidDate));
  const [refundDate, refundDateHandler] = useInput(
    useInputInit(invoice.refundDate)
  );
  const [refundNotes, refundNotesHandler] = useInput(
    useInputInit(invoice.refundNotes)
  );
  const [price, priceHandler] = useInput(useInputInit(invoice.price));
  const [totalPrice, totalPriceHandler] = useInput(
    useInputInit(invoice.totalPrice)
  );
  const [card, cardHandler] = useInput(useInputInit(invoice.card));
  const [transactionId, transactionIdHandler] = useInput(
    useInputInit(invoice.transactionId)
  );
  const [purchaseOrder, purchaseOrderHandler] = useInput(
    useInputInit(invoice.purchaseOrder)
  );
  const [checkNumber, checkNumberHandler] = useInput(
    useInputInit(invoice.checkNumber)
  );
  const [eftAch, eftAchHandler] = useInput(useInputInit(invoice.eftAch));
  const [notes, notesHandler] = useInput(useInputInit(invoice.notes));
  const [paid, paidHandler] = useInput(useInputInit(invoice.paid), "checkbox");
  const [refund, refundHandler] = useInput(
    useInputInit(invoice.refund),
    "checkbox"
  );

  const cls = useRef("");
  const promoId = useRef("");
  const students = useRef([]);

  const pmrAddress = useRef({});
  const pmrContact = useRef({});

  const type = useRef("");

  const cb = useCallback(getData, []);
  const col = "col-md-4";

  const del = async () => {
    if (window.confirm(`Is it okay to delete the Invoice `)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/invoices/${params.invoiceNum}` },
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
      validateAddress(pmrAddress.current, setAlertMessage, setShowAlert);
      validateContact(pmrContact.current, setAlertMessage, setShowAlert);

      const newinvoice = {
        pmrAgency,
        paymentMethod,
        paidDate,
        refundDate,
        refundNotes,
        price,
        totalPrice,
        card,
        transactionId,
        purchaseOrder,
        checkNumber,
        eftAch,
        notes,
        paid,
        promodId: parseInt(promoId.current),
        refund,
        pmrAddress: pmrAddress.current,
        pmrContact: pmrContact.current,
        type: type.current,
        cls: parseInt(cls.current),
        attendees: adjust(students.current, mode).map((x) => {
          delete x["action"];
          return x;
        }),
      };
      console.log("old", newinvoice);
      checkAddEmpty(newinvoice);
      if (mode === "EDIT") {
        checkIfEdited(newinvoice, invoice);
      }
      console.log("new ", newinvoice);
      if (Object.keys(newinvoice).length !== 0) {
        if (mode === "ADD")
          await sendRequest(
            { method: "POST", url: "/invoice/", body: newinvoice },
            null
          );
        if (mode === "EDIT")
          await sendRequest(
            {
              method: "PUT",
              url: `/invoice/${params.invoiceNum}`,
              body: newinvoice,
            },
            null
          );
        console.log("<<<<sent req in submit>>>>>>");
        setShowAlert(true);
        setAlertMessage("Saved Successfully ");
      }
    } catch (error) {}
  };
  return (
    <>
      <div className="container-fluid p-5">
        <BreadCrumbs list={list} />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form className="cd" onSubmit={submitHandler}>
          <div className="row p-0 m-0">
            <div className="col-md-8 text-center p-0 m-0">
              <h4 className="p-0 m-0">Pmr Details</h4>
            </div>
          </div>
          <div className="row p-0 ">
            <div className="col-md">
              <Col
                col={"col-md"}
                label="Agency"
                value={pmrAgency}
                onChange={pmrAgencyHandler}
                required={true}
              />
              <div className="col-md p-0 m-0">
                <Address
                  init={invoice.pmrAddress}
                  cb={cb}
                  cbref={pmrAddress}
                  mode={mode}
                />
              </div>
            </div>
            <div className="col-md">
              {" "}
              <Contact
                init={invoice.pmrContact}
                cb={cb}
                cbref={pmrContact}
                mode={mode}
              />
            </div>
            <div className="col-md">
              <div className="row">
                <Col
                  col={"col-md-6"}
                  label="Refund Notes"
                  value={refundNotes}
                  onChange={refundNotesHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Price"
                  value={price}
                  onChange={priceHandler}
                  required={true}
                />
                <Col
                  col={"col-md-6"}
                  label="Total Price"
                  value={totalPrice}
                  onChange={totalPriceHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Card"
                  value={card}
                  onChange={cardHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Transaction Id"
                  value={transactionId}
                  onChange={transactionIdHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Purchase Order"
                  value={purchaseOrder}
                  onChange={purchaseOrderHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Check Number"
                  value={checkNumber}
                  onChange={checkNumberHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="EftAch"
                  value={eftAch}
                  onChange={eftAchHandler}
                />
                <Col
                  col={"col-md-6"}
                  label="Notes"
                  value={notes}
                  onChange={notesHandler}
                />
                <Col
                  col="col-md-6"
                  label="Payment Method"
                  value={paymentMethod}
                  onChange={paymentMethodHandler}
                />
                <Col
                  col="col-md-6"
                  label="Paid Date"
                  value={paidDate}
                  onChange={paidDateHandler}
                  type="date"
                />
                <Col
                  col="col-md-6"
                  label="Refund Date"
                  value={refundDate}
                  onChange={refundDateHandler}
                  type="date"
                />
                <Col
                  col={"col-md-6"}
                  label="Paid"
                  value={paid}
                  onChange={paidHandler}
                  type="checkbox"
                />
                <Col
                  col={"col-md-6"}
                  label="Refund"
                  value={refund}
                  onChange={refundHandler}
                  type="checkbox"
                />
              </div>
            </div>
          </div>
          <div className="row">
            <SelectOne
              col={col}
              cb={cb}
              cbref={cls}
              data={invoice.cls}
              selectEntitys={selectClasses}
              val="id"
              show="id"
              comp="id"
              title="Class"
              initTxt="Select Class"
            />
            <SelectOne
              col={col}
              cb={cb}
              cbref={type}
              selectEntitys={selectInvoiceType}
              data={invoice.type}
              comp="type"
              show="type"
              val="type"
              title="Type"
              required={true}
              initTxt="-Select Type-"
            />
            <SelectOne
              col={col}
              cb={cb}
              cbref={promoId}
              data={invoice.promoId}
              selectEntitys={selectPromos}
              val="id" // code?
              show="code"
              comp="id" //code?
              title="Promo Code"
              initTxt="-Select Promo Code-"
            />
          </div>
          <div className="row">
            {mode === "ADD" && (
              <SelectEntity
                selectEntitys={selectStudents}
                named={["firstName", "lastName", "email"]}
                data={invoice.attendees}
                mode={mode}
                cb={cb}
                title="Attendees"
                cbref={students}
              />
            )}
            {mode === "EDIT" && (
              <>
                <div className="col-md-4">
                  <h5>Created</h5>
                  <h6>{invoice.created}</h6>
                </div>
                <div className="col-md-4">
                  <h5>Created By</h5>
                  <h6>
                    {`${invoice.createdBy.firstName} ${invoice.createdBy.lastName}`}
                  </h6>
                </div>
              </>
            )}
          </div>

          <button type="submit" className="btn btn-primary">
            Save
          </button>
          {mode === "EDIT" && (
            <button className="btn btn-danger mx-5" type="button" onClick={del}>
              Delete invoice
            </button>
          )}
        </form>
      </div>
    </>
  );
};

export default InvoiceDetailPage;
