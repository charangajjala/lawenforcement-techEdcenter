//import { useState } from "react";
import axios, { axiosFile } from "../util/axios";
import { useCallback, useContext } from "react";
import AuthContext from "../store/auth-store";
import { giveBuffer } from "../util/helper-functions/util-functions";
console.log("-------in usehttp outside-----");
const useHttp = (setAlertMessage, setShowAlert) => {
  /* const [isLoading,setLoading] = useState(false);
    const [err,setErr]=useState(null); */
  console.log("------in useHttp-------------");
  const authCtx = useContext(AuthContext);
  const sendRequest = useCallback(
    async (req, giveResponse, activeOnly) => {
      try {
        console.log(req);
        console.log("sent " + req.method + " request to url: ", req.url);
        console.log("sent req with token ;", localStorage.getItem("access"));
        const res = await axios({
          method: req.method || "GET",
          url: req.url,
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
          data: req.body || null,
          params: req.params || null,
        });
        console.log("got response : ", res.data);
        if (giveResponse) {
          if (activeOnly)
            giveResponse(res.data.filter((item) => item.isActive));
          else giveResponse(res.data);
        }
      } catch (error) {
        console.log("!!!!!!error in send request catch block!!!!!!", error);
        console.log("e.r.s", error.response);
        if (error.response && error.response.status === 401) {
          console.log("runnig getislogin");
          try {
            await authCtx.getIsLogin();
            await sendRequest(req, giveResponse).catch((e) => {});
            return;
          } catch (error) {
            console.log("error from getislogin in usehttp ", error);
            if (error.response && error.response.status === 401) {
              console.log("Logging out");
            } else {
              setAlertMessage({ e: true, message: "An Error Occured" });
              setShowAlert(true);
            }
          }
        }

        setShowAlert(true);
        if (error.response && error.response.status === 400) {
          const alertMessages = [].concat.apply(
            [],
            giveBuffer(error.response.data)
          );
          setAlertMessage(alertMessages);
        } else setAlertMessage({ e: true, message: "An Error Occured" });

        return Promise.reject(error);
      }
    },
    [authCtx, setAlertMessage, setShowAlert]
  );

  const fileRequest = useCallback(
    async (req, giveResponse, filenamed) => {
      try {
        console.log("sent " + req.method + " request to url: ", req.url);
        console.log(
          "sent req to " +
            req.url +
            "with token" +
            localStorage.getItem("access")
        );

        req.prevBody = req.body;
        const formdata = new FormData();
        if (filenamed) {
          formdata.append("file", req.body, filenamed);
          req.body = formdata;
        } else {
          formdata.append("file", req.body);
          req.body = formdata;
        }

        console.log("check new", req.body instanceof FormData);
        console.log("req.body", req.body);
        const res = await axiosFile({
          method: req.method || "GET",
          url: req.url,
          params: req.params || null,
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
          data: req.body || null,
        });
        console.log("got response : ", res.data);
        if (giveResponse) {
          giveResponse(res.data);
        }
      } catch (error) {
        console.log("!!!!!!error in send request catch block!!!!!!", error);
        console.log("e.r.s", error.response);

        if (error.response && error.response.status === 401) {
          console.log("runnig getislogin");
          try {
            await authCtx.getIsLogin();
            req.body = req.prevBody;
            await fileRequest(req, giveResponse, filenamed).catch((e) => {});
            return;
          } catch (error) {
            console.log("error from getislogin in usehttp ", error);
            if (error.response && error.response.status === 401) {
              console.log("Logging out");
            } else {
              setAlertMessage({ e: true, message: "An Error Occured" });
              setShowAlert(true);
            }
          }
        }

        setShowAlert(true);

        if (error.response && error.response.status === 400) {
          const alertMessages = [].concat.apply(
            [],
            giveBuffer(error.response.data)
          );
          setAlertMessage(alertMessages);
        } else setAlertMessage({ e: true, message: "An Error Occured" });

        return Promise.reject(error);
      }
    },
    [authCtx, setAlertMessage, setShowAlert]
  );

  return [sendRequest, fileRequest];
};

export default useHttp;
