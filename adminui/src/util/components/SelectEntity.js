import React, { useState, useEffect } from "react";
import TopicRow from "./TopicRow";
import useInput from "../../hooks/use-input";

const SelectEntity = ({
  title,
  selectEntitys,
  named,
  mode,
  data,
  cb,
  cbref,
  col,
  required,
}) => {
  const [entitys, setEntitys] = useState([]);
  const [entityField, entityFieldHandler, setEntityField] = useInput();

  useEffect(() => {
    if (mode === "EDIT" && data) {
      setEntitys(
        data.map((entity) => {
          return { ...entity, action: "ADD", old: true };
        })
      );
    }
  }, [data, mode]);

  useEffect(() => {
    if (entitys) {
      cb(cbref, entitys);
    }
  }, [cb, cbref, entitys]);

  const entityAddHandler = () => {
    if (!entityField) return;
    const newEntitys = [...entitys];

    const existingEntity = newEntitys.find(
      (entity) => String(entity.id) === entityField
    );
    if (!existingEntity) {
      const newEntity = { id: parseInt(entityField), action: "ADD" };
      if (Array.isArray(named)) {
        for (const name of named) {
          newEntity[name] = selectEntitys.find(
            (entity) => String(entity.id) === entityField
          )[name];
        }
      } else {
        newEntity[named] = selectEntitys.find(
          (entity) => String(entity.id) === entityField
        )[named];
      }
      newEntitys.push(newEntity);
    }

    if (existingEntity) {
      existingEntity.action = "ADD";
    }
    setEntitys(newEntitys);
    setEntityField("");
  };

  const entityDeleteHandler = (id) => {
    const newEntitys = [...entitys];
    newEntitys.find((entity) => entity.id === id).action = "DELETE";
    setEntitys(newEntitys);
  };
  console.log("check", entitys);
  return (
    <div className={col || "col-md-4 h-100 "}>
      <h6 className="p-0 m-0">{title}</h6>
      <div style={{ maxHeight: "300px" }}>
        {entitys.map(
          (entity) =>
            entity.action !== "DELETE" && (
              <TopicRow
                key={entity.id}
                id={entity.id}
                name={
                  Array.isArray(named)
                    ? `${entity["firstName"]} ${entity["lastName"]}` // invoice(Post) specific
                    : entity[named]
                }
                deleteHandler={entityDeleteHandler}
              />
            )
        )}
      </div>
      <div className="row">
        <div className="col-8">
          <select
            className="form-select"
            onChange={entityFieldHandler}
            value={entityField}
            required={!!required && !entitys.some(ent=> ent.action=== "ADD")}
          >
            <option value={""} defaultValue>
              Select Entitys
            </option>
            {selectEntitys.map((entity) => {
              const exists = entitys.find((en) => en.id === entity.id);

              return !exists || exists.action !== "ADD" ? (
                <option key={entity.id} value={entity.id}>
                  {Array.isArray(named)
                    ? `${entity[named[0]]} ${entity[named[1]]}`
                    : entity[named]}
                </option>
              ) : null;
            })}
          </select>
        </div>
        <div className="col-4">
          <button
            className="btn btn-dark"
            type="button"
            onClick={entityAddHandler}
          >
            Add
          </button>
        </div>
      </div>
    </div>
  );
};

export default SelectEntity;
