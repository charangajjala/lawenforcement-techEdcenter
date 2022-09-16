import React, { useState, useEffect } from "react";
import { useParams, useLocation, Redirect } from "react-router-dom";
import BreadCrumbs from "../util/components/BreadCrumbs";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";
import useHttp from "../hooks/use-http";
import fileDownload from "js-file-download";

export const OldInvoice = () => {
  const qparams = new URLSearchParams(useLocation().search);
  return (
    <Redirect
      to={`/invoice/${qparams.get("id")}/${qparams.get("access_key")}`} // class Id??
    ></Redirect>
  );
};

const InvoicePage = () => {
  const [invoice, setInvoice] = useState({
    pmrContact: {},
    pmrAddress: {},
    attendees: [],
  });
  const [discount, setDiscount] = useState({});
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const list = ["Home", "Invoice"];

  const { invoiceNum, accessKey, clsid } = useParams();

  useEffect(() => {
    sendRequest(
      { url: `/invoice/`, params: { invoiceNum, accessKey } },
      setInvoice
    ).catch((_) => {});
  }, [sendRequest, accessKey, invoiceNum, clsid]);

  useEffect(() => {
    if (invoice.cls && invoice.code) {
      sendRequest({ url: `/promos/${invoice.code}/` }, setDiscount).catch(
        (_) => {}
      );
    }
  }, [sendRequest, invoice]);

  const pmrc = invoice.pmrContact;
  const pmra = invoice.pmrAddress;

  const downloadInvoice = async (e) => {
    try {
      await sendRequest(
        {
          url: `invoice/download/${invoiceNum}/`,
          body: { clsid },
          method: "POST",
          responseType: "blob",
        },
        (res) => {
          fileDownload(res, "invoice.pdf");
        }
      );
    } catch (error) {}
  };

  const calDiscount = (disc) => {
    if (!disc.type) return 0;
    const { type, value } = disc;
    let discount = 0;
    if (type === "Seats") {
      discount = parseFloat(value) * parseFloat(invoice.price);
    } else if (type === "Flat") {
      discount = parseFloat(value);
    } else {
      discount = (parseFloat(invoice.price) * parseFloat(value)) / 100;
    }
    return discount;
  };

  return (
    <div>
      <BreadCrumbs list={list} title="Invoice" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <div className="container">
        <div className="row">
          {pmrc && pmra && (
            <div className="col-sm-4">
              <p>
                <strong>{pmrc.name}</strong>
                <br />
                {invoice.pmrAgency}
                <br />
                {pmra.address1}
                <br />
                {`${pmra.city} ${pmra.state} ${pmra.zip}`}
                <br />
                {pmrc.email}
                <br />
                {pmrc.phone}
              </p>
            </div>
          )}
          <div className="col-sm-4"></div>
          <div className="col-sm-4">
            <table id="invoice-download-pay">
              <tr>
                <td>
                  <button className="btn btn-primary" onClick={downloadInvoice}>
                    Download as PDF
                  </button>
                </td>
              </tr>
              {!invoice.paid && (
                <tr>
                  <td>
                    <a href="#" className="btn btn-success">
                      Pay For This Invoice
                    </a>
                  </td>
                </tr>
              )}
            </table>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-12">
            <table className="table table-borderless table-striped table-sm">
              <tr>
                <th style={{ width: "55%" }}>Description</th>
                <th style={{ width: "15%" }}>Quantity</th>
                <th style={{ width: "15%" }}>Price</th>
                <th style={{ width: "15%" }}>Subtotal</th>
              </tr>
              <tr>
                <td style={{ width: "55%" }}>
                  <strong>Class:</strong>
                  <br />
                  {invoice.cls}
                  <br />
                  {invoice.startDate} to {invoice.endDate}
                  <br />
                  <br />
                </td>
                <td style={{ width: "15%" }}>{invoice.attendees.length}</td>
                <td style={{ width: "15%" }}>${invoice.price}</td>
                <td style={{ width: "15%" }}>
                  ${parseFloat(invoice.price) * invoice.attendees.length}
                </td>
              </tr>
              {invoice.attendees && (
                <tr>
                  <td style={{ width: "55%" }}>
                    <strong>Attendees:</strong>
                    <br />
                    {invoice.attendees.map((attendee, i) => (
                      <div key={i}>
                        {`${attendee.firstName} ${attendee.lastName}`} -
                        {attendee.email} <br />
                      </div>
                    ))}
                  </td>
                  <td style={{ width: "15%" }}></td>
                  <td style={{ width: "15%" }}></td>
                  <td style={{ width: "15%" }}></td>
                </tr>
              )}
              {invoice.code !== undefined && (
                <tr>
                  <td style={{ width: "55%" }}>
                    Promo: <i>{discount.code}</i>
                  </td>
                  <td style={{ width: "15%" }}></td>
                  <th style={{ width: "15%" }}>Discount:</th>
                  <td style={{ width: "15%" }}>
                    {`-$${calDiscount(discount)}`}
                  </td>
                </tr>
              )}
              <tr>
                <td style={{ width: "55%" }}></td>
                <td style={{ width: "15%" }}></td>
                <th style={{ width: "15%" }}>Total: </th>
                <th style={{ width: "15%" }}>{`$${
                  invoice.totalPrice ||
                  invoice.inserviceFee - calDiscount(discount)
                }`}</th>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InvoicePage;
