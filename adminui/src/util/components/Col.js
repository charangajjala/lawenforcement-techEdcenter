import React, { useState } from "react";

const Col = ({
  col,
  label,
  type,
  value,
  disabled,
  onChange,
  rows,
  required,
  maxlen
}) => {
  const [showPass, setShowPass] = useState(false);

  const other = {
    type: type ? type : "text",
    value,
    maxLength: maxlen || "256",
    required: required ,
  };
  const checkbox = {
    type: "checkbox",
    checked: value,
  };
  const num = {
    type: "number",
    min: "1",
    value,
    required: required,
  };
  const password = {
    type: showPass ? "text" : "password",
    minLength: "6",
    maxLength: "20",
    required: required,
    value,
  };
  const fit =
    type === "checkbox"
      ? checkbox
      : type === "num"
      ? num
      : type === "password"
      ? password
      : other;

  const showPassword = (e) => {
    setShowPass((prev) => !prev);
  };
  const jsx = (
    <>
      <div
        className={` ${
          type === "password"
            ? "col-11 p-0" 
            : type === "checkbox"
            ? "d-inline"
            : "p-0"
        }`}
      >
        <input
          className={type === "checkbox" ? "form-check-input" : "form-control"}
          id={label}
          {...fit}
          disabled={disabled ? true : false}
          onChange={onChange}
        />
      </div>
      {type === "password" && (
        <div className="input-group-text col-1 p-0 bg-white border-0">
          <i
            className={`bi ${showPass ? "bi-eye-slash-fill" : "bi-eye-fill"}`}
            onClick={showPassword}
            style={{ fontSize: "1.5rem" }}
          ></i>
        </div>
      )}
    </>
  );
  return (
    <div className={col}>
      <label htmlFor={label} className="p-0 m-0">
        <h6 className="p-0 m-0">{label}</h6>
      </label>
      {type !== "textarea" ? (
        type === "password" ? (
          <div className="row">{jsx}</div>
        ) : (
          jsx
        )
      ) : (
        <textarea
          value={value}
          onChange={onChange}
          id={label}
          required={required !== undefined ? required : false}
          rows={rows || 2}
          className="form-control"
          style={{ resize: "none" }}
          maxLength = "511"
        />
      )}
    </div>
  );
};

export default Col;
