import React, { useState, useEffect, useRef } from "react";
import dp from "../../images/defaultdp.jpg";

const Upload = ({ title, cb, cbref, data, col,required }) => {
  const [entity, setEntity] = useState({});

  const entityRef = useRef();

  useEffect(() => {
    if (data) setEntity({ url: data, showEntity: false });
    else setEntity({ url: null, showEntity: true });
  }, [data]);

  useEffect(() => {
    if (entity && entity.file) {
      cb(cbref, entity.file);
    }
  }, [cb, cbref, entity]);

  const toggleEntity = () => {
    setEntity({ ...entity, showEntity: !entity.showEntity });
  };

  const addEntity = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setEntity({
      // doubt
      url: "dummy",
      showEntity: !entity.showEntity,
      file: entityRef.current.files[0],
    });
  };
  return (
    <div className={col || "col-md-4"}>
      <h6 className="p-0 m-0">{title}</h6>
      {!entity.url ? ( // no !
        <img
          src={/* entity.url */ dp}
          alt="Loading..."
          width="200px"
          height="200px"
        />
      ) : (
        <h6 className="p-0 m-3">Upload Image</h6>
      )}
      {!entity.url && ( // no !
        <button type="button" className="btn btn-dark d-block btn-sm mx-5 " onClick={toggleEntity}>
          {`Change ${title}`}
        </button>
      )}
      {!entity.showEntity && ( // no !
        <form onSubmit={addEntity}>
          <input type="file" ref={entityRef} required={required} />
          <button type="submit" className="btn btn-dark btn-sm mx-2">
            Upload
          </button>
        </form>
      )}
    </div>
  );
};

export default Upload;
