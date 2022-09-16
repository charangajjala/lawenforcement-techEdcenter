import React, { useState, useCallback } from "react";
import { axiosDefault } from "../util/axios";

const AuthContext = React.createContext({
  isLogin: false,
  login: (access, refresh) => {},
  getIsLogin: () => {},
  getProfiles: () => {},
  logout: () => {},
  error: { set: false, data: null },
  user: {},
});
console.log("in authstore outside");

export const AuthContextProvider = (props) => {
  console.log("----------in authstore----------");
  const initAccess = localStorage.getItem("access");
  const [isLogin, setIsLogin] = useState(!!initAccess);
  const [error, setError] = useState({ set: false, data: null });
  const [user, setUser] = useState(
    localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {roles:{}}
  );

  /* const getProfiles = async (sendRequest) => {
    const whichprofiles = {
      instructor: true,
      student: true,
      host: true,
      stop: false,
    };
    await sendRequest({ url: "/instructors/" }).catch((error) => {
      whichprofiles.instructor = false;
    });
    await sendRequest({ url: "/students/" }).catch((error) => {
      whichprofiles.student = false;
    });
    await sendRequest({ url: "/hosts/" }).catch((error) => {
      whichprofiles.host = false;
    });
    whichprofiles.stop = true;
    setWhichProfiles(whichprofiles);
  }; */

  const logout = useCallback(() => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    setIsLogin(false);
    setUser({});
  }, []);

  const getIsLogin = useCallback(async () => {
    if (!localStorage.getItem("refresh")) throw new Error("no refresh token");
    console.log("in getIsLogin");
    try {
      const res = await axiosDefault.post("authentication/refresh/", {
        refresh: localStorage.getItem("refresh"),
      });
      if (res.data.access) {
        console.log(
          "setting access into localStorage by getIsLogin ",
          res.data.access
        );
        localStorage.setItem("access", res.data.access);
      }
    } catch (e) {
      console.log("in getinlogin error ", e, "e.response", e.response);
      if (e.response && e.response.status === 401) {
        logout();
        return Promise.reject(e);
      }
      return Promise.reject(e);
    }
  }, [logout]);

  const login = (access, refresh, user) => {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    const rolesobj = {};
    if (user.roles.length > 0) {
      for (const role of ["host", "student", "instructor"]) {
        if (user.roles.includes(role)) {
          rolesobj[role] = true;
        }
      }
    } else {
      rolesobj["nouser"] = true;
    }
    delete user["roles"];
    const setuser = { ...user, roles: rolesobj };

    localStorage.setItem("user", JSON.stringify(setuser));
    setUser(setuser);
    setIsLogin(true);
  };

  const putError = (err) => {
    setError({ set: true, data: err });
  };

  const ctxVal = {
    login,
    isLogin,
    logout,
    getIsLogin,
    error,
    putError,
    /* getProfiles, */
    user,
  };

  return (
    <AuthContext.Provider value={ctxVal}>{props.children}</AuthContext.Provider>
  );
};
export default AuthContext;
