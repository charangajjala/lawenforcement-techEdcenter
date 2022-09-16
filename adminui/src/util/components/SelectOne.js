import React, { useEffect } from "react";
import useInput from "../../hooks/use-input";

const SelectOne = ({
  selectEntitys,
  data,
  cb,
  cbref,
  col,
  title,
  comp,
  show,
  val,
  titlecol,
  initTxt,
  required,
}) => {
  console.log("here", data);
  const [entityField, entityFieldHandler] = useInput(
    data !== undefined && selectEntitys.length > 0
      ? selectEntitys.find((entity) => entity[comp] === data)[val]
      : selectEntitys.length > 0 && !initTxt
      ? selectEntitys[0][val]
      : null
  );
  
  useEffect(() => {
    if (entityField !== undefined) {
      if (cbref) cb(cbref, entityField);
      else cb(entityField);
    }
  }, [cb, cbref, entityField]);

  return (
    <div className={col}>
      {titlecol ? <h6 className={titlecol}>{title}</h6> : <h6 className="m-0 p-0">{title}</h6>}
      <div className="p-0 " >
        <select
          className="form-select form-control" 
          onChange={entityFieldHandler}
          value={entityField}
          required={required}
        >
          {initTxt && (
            <option selected={data === undefined} value={""}>
              {initTxt}
            </option>
          )}
          {selectEntitys.map((entity) => (
            <option
              key={entity[comp]}
              value={entity[val]}
              selected={data !== undefined && data === entity[comp]}
            >
              {entity[show]}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default SelectOne;
