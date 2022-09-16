import React from "react";
import ReactDOM from "react-dom";

const Modal = ({
  Component,
  props = { mode: "ADD" },
  mdltitle,
  thisModal,
  onClose,
}) => {
  const modalContent = (
    <div
      className="modal fade "
      id={thisModal ? thisModal : `${props.mode}`}
      tabIndex="-1"
      role="dialog"
      aria-labelledby="exampleModalLongTitle"
      aria-hidden="true"
    >
      <div className="modal-dialog mw-100 w-75" role="document">
        <div className="modal-content ">
          <div className="modal-header">
            <h5 className="modal-title" id="exampleModalLongTitle">
              {mdltitle}
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
            <Component isModal={true} {...props} />
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
      {(props.mode !== "EDIT") | !!thisModal && (
        <button
          type="button"
          className="btn btn-primary btn-sm "
          data-toggle="modal"
          data-backdrop="static"
          data-keyboard="false"
          data-target={thisModal ? `#${thisModal}` : `#ADD`}
        >
          {mdltitle}
        </button>
      )}

      {ReactDOM.createPortal(modalContent, document.getElementById("modal"))}
    </div>
  );
};

export default Modal;
