import { useState } from "react";

const useAlert = ( refresh ) => {
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState("");

  if (showAlert) {
    setTimeout(() => {
      if (refresh) {
        window.location.reload();
        return;
      }
      setShowAlert(false);
    }, 5000);
  }

  return [showAlert, setShowAlert, alertMessage, setAlertMessage];
};

export default useAlert;
