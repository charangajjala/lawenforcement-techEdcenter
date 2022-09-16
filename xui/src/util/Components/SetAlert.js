import React from "react";
import Alert from "./Alert";

const SetAlert = ({ alertMessage, showAlert }) => {
  return (
    <>
      {showAlert &&
        (Array.isArray(alertMessage) ? (
          alertMessage.map((msg,i) => <Alert message={msg} key={i} />)
        ) : (
          <Alert alert={alertMessage} />
        ))}
    </>
  );
};

export default SetAlert;
