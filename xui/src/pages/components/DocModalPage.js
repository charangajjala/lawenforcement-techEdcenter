import React, { useRef, useCallback } from "react";
import SetAlert from "../../util/components/SetAlert";
import useAlert from "../../hooks/use-alert";
import useHttp from "../../hooks/use-http";
import FileUpload from "../../util/components/FileUpload";
import { getData, adjust } from "../../util/helper-functions/util-functions";

const DocPage = ({ initdocs, url, params }) => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest, fileRequest] = useHttp(setAlertMessage, setShowAlert);
  const docs = useRef([]);
  const cb = useCallback(getData, []);

  const submit = async () => {
    try {
      if (docs.current.length === 0) return;
      const setDocId = (doc, id) => {
        doc.id = id.id;
      };

      for (const doc of docs.current) {
        if (doc && doc.old !== true && doc.action === "ADD") {
          await fileRequest(
            { url: "/file/", method: "POST", body: doc.file },
            setDocId.bind(null, doc),
            doc.name
          );
        }
      }
      const req = {
        url,
        method: "POST",
        body: { docs: adjust(docs.current, "EDIT") },
        params,
      };

      await sendRequest(req, null);
      setShowAlert(true);
      setAlertMessage("Saved Successfully");
    } catch (error) {}
  };
  return (
    <div className="container">
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <FileUpload
        cbref={docs}
        cb={cb}
        col="col-12"
        title="Class Materials"
        data={initdocs}
        mode="EDIT"
      />
      <button className="btn btn-primary" onClick={submit}>
        Save
      </button>
    </div>
  );
};

export default DocPage;
