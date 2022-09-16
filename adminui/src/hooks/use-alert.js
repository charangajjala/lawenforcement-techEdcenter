import { useState, useEffect } from "react";

const useAlert = (refresh) => {
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState("");

  useEffect(() => {
    if (showAlert) {
      console.log("alertMessage", alertMessage);
      setTimeout(() => {
        if (refresh && !alertMessage.e) {
          window.location.reload();
          return;
        }
        setShowAlert(false);
      }, 5000);
    }
  }, [alertMessage, showAlert, refresh]);

  return [showAlert, setShowAlert, alertMessage, setAlertMessage];
};

export default useAlert;
