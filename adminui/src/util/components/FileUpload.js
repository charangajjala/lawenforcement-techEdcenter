import React, { useEffect, useState, useRef } from "react";
import useInput from "../../hooks/use-input";
import TopicRow from "./TopicRow";

const FileUpload = ({ mode, data, cb, cbref, title, maxheight, required }) => {
  const [materials, setMaterials] = useState([]);
  const [materialField, materialFieldHandler, setMaterialField] = useInput();
  const materialFile = useRef();

  useEffect(() => {
    if (mode === "EDIT" && data) {
      setMaterials(
        data.map((material) => {
          return { ...material, action: "ADD", old: true };
        })
      );
    }
  }, [data, mode]);

  useEffect(() => {
    if (materials) {
      cb(cbref, materials);
    }
  }, [cb, cbref, materials]);

  const materialAddHandler = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const file = materialFile.current.files[0];
    if (!file | materialField) return;
    console.log(file);
    const newMaterials = [...materials];
    const newMaterial = {
      id: Math.random(),
      name: materialField,
      action: "ADD",
      fname: file.name,
      file,
    };
    newMaterials.push(newMaterial);
    setMaterials(newMaterials);
    setMaterialField("");
    materialFile.current.value = "";
  };

  const materialDeleteHandler = (id) => {
    const newMaterials = [...materials];
    const newMaterial = newMaterials.find((material) => material.id === id);
    newMaterial.action = "DELETE";
    setMaterials(newMaterials);
  };

  return (
    <div className="col-md-4">
      <h6 className="p-0 m-0">{title}</h6>
      <div
        style={{
          maxHeight: maxheight || "300px",
          overflowY: "auto",
          overflowX: "hidden",
        }}
        className="p-0 m-0"
      >
        {materials.map((material) => {
          return (
            material.action !== "DELETE" && (
              <TopicRow
                key={material.id}
                id={material.id}
                name={`${material.name}  ${
                  material.fname ? `(${material.fname})` : ""
                }`}
                deleteHandler={materialDeleteHandler}
              />
            )
          );
        })}
      </div>
      <form onSubmit={materialAddHandler}>
        <div className="row p-0 m-0">
          <div className="col-xl-6">
            <input
              type="file"
              ref={materialFile}
              required={!!required && materials.length > 0}
            />
          </div>
          <div className="col-xl-6">
            <input
              type="text"
              placeholder="Material Name"
              className="w-100"
              required
              onChange={materialFieldHandler}
              value={materialField}
            />
          </div>
          <div className="col d-flex justify-content-end">
            <input className="btn btn-dark" type="submit" value="Add" />
          </div>
        </div>
      </form>
    </div>
  );
};

export default FileUpload;
