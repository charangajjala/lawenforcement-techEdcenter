import React, { useState, useEffect } from "react";

const FilterInput = ({
  type,
  col,
  options,
  label,
  filtref,
  show,
  val,
  required,
  onBlur,
}) => {
  const [value, setValue] = useState("");

  const handler = (e) => {
    setValue(e.target.value);
    filtref.current.value = e.target.value;
  };
  useEffect(() => {
    if (filtref.current.value !== undefined) {
      setValue(filtref.current.value);
    }
  }, [filtref.current.value, filtref]);

  const other = type !== "select" && !show;
  return (
    <div className={col} >
      {other && (
        <>
          {type === "date" && <p>Created At</p>}
          <input
            type={type ? type : "text"}
            placeholder={label}
            onChange={handler}
            className="form-control"
            required={required ? required : false}
            value={value}
            onBlur={onBlur}
          />
        </>
      )}
      {type === "select" && (
        <select onChange={handler} className="form-select">
          {options.map((option, i) => (
            <option value={i === 0 ? "" : option} key={i}>
              {option.toUpperCase()}
            </option>
          ))}
        </select>
      )}
      {show !== undefined && (
        <select
          className="form-select"
          onChange={handler}
          required={required ? true : false}
          value={value}
        >
          <option value="">{label}</option>
          {options.map((option) => (
            <option value={option[val]} key={option[val]}>
              {option[show]}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

export default FilterInput;
