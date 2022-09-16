import React, { useEffect, useState } from "react";

const Desc = ({
  title,
  descData,
  cb,
  col,
  cbref,
  placeholder,
  maxheight,
  required,
}) => {
  const [descObj, setDescObj] = useState({});
  console.log("desc running");
  useEffect(() => {
    if (descObj) {
      if (cbref) cb(cbref, descObj);
      else cb(descObj);
    }
  }, [cb, descObj, cbref]);

  useEffect(() => {
    const newDescObj = {};
    if (descData) {
      let i = 0;

      for (const desc of descData) {
        i++;
        newDescObj[i] = desc;
      }
    }
    newDescObj["lkey"] = 1;
    newDescObj[`extra${newDescObj["lkey"]}`] = "";

    setDescObj(newDescObj);
  }, [descData]);

  const descHandlers = {};

  const helpMakeDescHandler = (newDescObj, key) => {
    return (e) => {
      newDescObj[key] = e.target.value;

      if (newDescObj[key] === "") {
        delete newDescObj[key];
      }
      if (key === `extra${newDescObj["lkey"]}`) {
        if (newDescObj[`extra${newDescObj["lkey"]}`] !== "") {
          newDescObj["lkey"] += 1;
          newDescObj[`extra${newDescObj["lkey"]}`] = "";
        }
      }

      setDescObj(newDescObj);
    };
  };

  for (const key in descObj) {
    if (key !== "lkey") {
      const newDescObj = { ...descObj };
      descHandlers[key] = helpMakeDescHandler(newDescObj, key);
    }
  }
  console.log("new", descObj);
  return (
    <div className={col || "col-md-4   "}>
      {title && <h6 className="p-0 m-0">{title}</h6>}
      <div
        style={{
          maxHeight: maxheight || "300px",
          overflowY: "auto",
          overflowX: "hidden",
        }}
      >
        {Object.keys(descObj).map((key, i) => {
          return (
            key !== "lkey" && (
              <div className="col-12 p-0 m-0" key={key}>
                <textarea
                  placeholder={placeholder}
                  value={descObj[key]}
                  onChange={descHandlers[key]}
                  className="w-100"
                  rows="2"
                  style={{ resize: "none" }}
                  required={
                    !!required &&
                    key === `extra${descObj["lkey"]}` &&
                    Object.keys(descObj).length === 2
                  }
                  maxlength="511"
                />
              </div>
            )
          );
        })}
      </div>
    </div>
  );
};

export default Desc;
