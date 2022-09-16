import React, { useState, useCallback } from "react";
import { axiosDefault } from "../util/axios";

const AuthContext = React.createContext({
  isLogin: false,
  login: (access, refresh) => {},
  getIsLogin: () => {},
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
    localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {}
  );

  const getIsLogin = useCallback(async () => {
    console.log("in getIsLogin");
    try {
      const res = await axiosDefault.post("admin/authentication/refresh/", {
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
  }, []);

  const login = (access, refresh, user) => {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    setIsLogin(true);
    localStorage.setItem("user", JSON.stringify(user));
    setUser(user);
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    setIsLogin(false);
    setUser({});
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
    user,
  };

  return (
    <AuthContext.Provider value={ctxVal}>{props.children}</AuthContext.Provider>
  );
};
export default AuthContext;
