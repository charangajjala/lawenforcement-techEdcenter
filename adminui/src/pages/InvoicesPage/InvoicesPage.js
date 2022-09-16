import React, { useState, useEffect, useRef } from "react";
import useHttp from "../../hooks/use-http";
import useAlert from "../../hooks/use-alert";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import TableRow from "../../util/components/TableRow";
import SetAlert from "../../util/components/SetAlert";
import FilterInput from "../../util/components/FilterInput";
import { selectInvoiceType } from "../../constants/selectConstants";

const InvoicesPage = () => {
  const [invoices, setInvoices] = useState([]);
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp();

  const list = ["Home", "Invoices"];

  const order = [
    "invoiceNum",
    "pmrAgency",
    "pmrContact",
    "type",
    "class",
    "paid",
    "refund",
    "totalPrice",
    "created",
  ];

  useEffect(() => {
    sendRequest({ url: "/invoice/" }, setInvoices).catch((e) => {});
  }, [sendRequest]);

  const del = async (invoiceNum) => {
    if (window.confirm(`Is it okay to delete the Invoice`)) {
      try {
        await sendRequest(
          { method: "DELETE", url: `/invoice/${invoiceNum}` },
          null
        );
        setShowAlert(true);
        setAlertMessage("Deleted Successfully");
        sendRequest({ url: "/invoice/" }, setInvoices);
      } catch (error) {}
    }
  };
  const filtcol = "col-auto";
  const sinvoiceNum = useRef({ value: "" });
  const spmrAgency = useRef({ value: "" });
  const spmrContact = useRef({ value: "" });
  const stype = useRef({ value: "" });
  const sclass = useRef({ value: "" });
  const spaid = useRef({ value: "" });
  const srefund = useRef({ value: "" });
  const stotalPrice = useRef({ value: "" });
  const screated = useRef({ value: "" });

  const resetFilters = (e) => {
    sinvoiceNum.current.value = "";
    spmrAgency.current.value = "";
    spmrContact.current.value = "";
    stype.current.value = "";
    sclass.current.value = "";
    spaid.current.value = "";
    srefund.current.value = "";
    stotalPrice.current.value = "";
    screated.current.value = "";
    formref.current.reset();
  }

  const formref = useRef();

  const searchHandler = (e) => {
    if (e) e.preventDefault();

    const params = {
      sinvoiceNum: sinvoiceNum.current.value,
      spmrAgency: spmrAgency.current.value,
      spmrContact: spmrContact.current.value,
      stype: stype.current.value,
      sclass: sclass.current.value,
      spaid: spaid.current.value,
      srefund: srefund.current.value,
      stotalPrice: stotalPrice.current.value,
      screated: screated.current.value,
    };
    for (const k in params) {
      const val = params[k];
      if (val === null || val === undefined || val === "") delete params[k];
    }
    console.log(params);
    try {
      sendRequest({ url: "/invoice/", params: params }, setInvoices);
    } catch (error) {}
  };
  return (
    <>
      <div className="container-fluid p-4">
        <BreadCrumbs list={list} addEntity="invoice" />
        <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
        <form onSubmit={searchHandler} ref={formref}>
          <div className="row">
            <FilterInput
              label="Invoice Num"
              filtref={sinvoiceNum}
              col={filtcol}
            />
            <FilterInput
              label="Pmr Agency"
              filtref={spmrAgency}
              col={filtcol}
            />
            <FilterInput
              label="Pmr Contact"
              filtref={spmrContact}
              col={filtcol}
            />
            <FilterInput
              label="Total Price"
              filtref={stotalPrice}
              col={filtcol}
            />
            <FilterInput
              col={filtcol}
              val="type"
              show="type"
              label="-Type-"
              options={selectInvoiceType}
              filtref={stype}
            />
            <FilterInput
              filtref={spaid}
              col={filtcol}
              type="select"
              options={["-Paid-", "true", "false"]}
            />
            <FilterInput
              filtref={srefund}
              col={filtcol}
              type="select"
              options={["-Refund-", "true", "false"]}
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
        <table className="table  table-striped m-2 ">
          <thead>
            <tr>
              <th scope="col"> Invoice Number</th>
              <th scope="col">Pmr Agency</th>
              <th scope="col">Pmr Contact</th>
              <th scope="col">Type</th>
              <th scope="col">Class</th>
              <th scope="col">Paid</th>
              <th scope="col">Refund</th>
              <th scope="col">Total Price</th>
              <th scope="col">Created</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((invoice) => (
              <TableRow
                key={invoice.invoiceNum}
                data={invoice}
                path="invoices"
                del={del}
                order={order}
              />
            ))}
            
          </tbody>
        </table>
        {invoices.length === 0 && (
            <div className="text-center  justify-content-center align-content-center px-5 m-5">
              <h4 className="display-4 px-5 mx-5">No Invoices Available</h4>
            </div>
          )}
      </div>
    </>
  );
};

export default InvoicesPage;
