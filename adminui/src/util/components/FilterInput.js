import React, { useRef } from "react";

const FilterInput = ({ type, col, options, label, filtref, show, val }) => {
  const handler = (e) => {
    filtref.current.value = e.target.value;
  };
  const other = type !== "select" && !show;
  const ref = useRef();
  return (
    <div className={col}>
      {other && (
        <>
          {/* {type === "date" && <label className="">{label|| 'Created At'}</label>} */}
          <input
            type={type !== "date" ? (type ? type : "text") : "text"}
            placeholder={label || "Created At"}
            onChange={handler}
            className="form-control my-1 "
            ref={ref}
            onFocus={
              type === "date"
                ? (_) => {
                    ref.current.type = "date";
                  }
                : null
            }
            onBlur={
              type === "date"
                ? (_) => {
                    ref.current.type = "text";
                  }
                : null
            }
          />
        </>
      )}
      {type === "select" && (
        <select onChange={handler} className="form-select my-1">
          {options.map((option, i) => (
            <option value={i === 0 ? "" : option} key={i}>
              {option.toUpperCase()}
            </option>
          ))}
        </select>
      )}
      {show !== undefined && (
        <select className="form-select my-1" onChange={handler}>
          <option value="">{label}</option>
          {options.map((option) => (
            <option value={option[val]} key={option.id}>
              {option[show]}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

export default FilterInput;
