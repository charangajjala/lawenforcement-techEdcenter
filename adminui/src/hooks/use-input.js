import { useState, useEffect } from "react";

const useInput = (data, type) => {
  const [enteredValue, setEnteredValue] = useState("");

  useEffect(() => {
    if ((data !== null) & (data !== undefined)) setEnteredValue(data);
  }, [data]);

  const valueChangeHandler = (e) => {
    setEnteredValue(
      type === "checkbox" ? (e.target.checked ? true : false) : e.target.value
    );
  };

  return [enteredValue, valueChangeHandler, setEnteredValue];
};

export default useInput;
