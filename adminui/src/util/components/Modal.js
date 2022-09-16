import React from "react";
import ReactDOM from "react-dom";

const Modal = ({
  Component,
  addBtnName,
  modalFunc,
  sub,
  props,
  thisModal,
  onClick,
  onClose,
  showComp,
  nobutton,
}) => {
  console.log("---Modal----");
  const modalContent = (
    <div
      className="modal fade "
      id={
        sub
          ? "exampleModalLongsub"
          : thisModal
          ? `exampleModalLong${thisModal}`
          : "exampleModalLong"
      }
      tabIndex="-1"
      role="dialog"
      aria-labelledby="exampleModalLongTitle"
      aria-hidden="true"
    >
      <div className="modal-dialog mw-100 w-75" role="document">
        <div className="modal-content ">
          <div className="modal-header">
            <h5 className="modal-title" id="exampleModalLongTitle">
              {addBtnName}
            </h5>
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label="Close"
              onClick={onClose || function () {}}
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body ">
            {(showComp === undefined || !showComp === false) && (
              <Component
                isModal={true}
                mode="ADD"
                modalFunc={modalFunc}
                {...props}
              />
            )}
          </div>
          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              data-dismiss="modal"
              onClick={onClose || function () {}}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
  return (
    <div>
      {nobutton !== true && (
        <button
          type="button"
          className="btn btn-primary btn-sm "
          data-toggle={sub ? "modal" : "modal"}
          data-backdrop="static"
          data-keyboard="false"
          data-target={
            sub
              ? "#exampleModalLongsub"
              : thisModal
              ? `#exampleModalLong${thisModal}`
              : "#exampleModalLong"
          }
          onClick={onClick || function () {}}
        >
          {addBtnName}
        </button>
      )}
      {ReactDOM.createPortal(
        modalContent,
        document.getElementById(`${sub ? "submodal" : "modaltest"}`)
      )}
    </div>
  );
};

export default Modal;
