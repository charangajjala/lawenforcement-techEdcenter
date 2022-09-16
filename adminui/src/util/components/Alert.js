import React from "react";

const Alert = ({ alert }) => {
  return (
    <div
      className={`alert text-center ${
        alert.e ? "alert-danger" : "alert-success"
      }`}
      role="alert"
    >
      {alert.e ? alert.message : alert}
    </div>
  );
};

export default Alert;
