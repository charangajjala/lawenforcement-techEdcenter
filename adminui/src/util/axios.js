import axio from "axios";
console.log("in axios");
const axios = axio.create({
  baseURL: "http://localhost:8000/admin",
  headers: {
    "Content-Type": "application/json",
  },
});

export const axiosFile =   axio.create({
  baseURL: "http://localhost:8000/admin",
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export const axiosDefault = axio.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default axios;
