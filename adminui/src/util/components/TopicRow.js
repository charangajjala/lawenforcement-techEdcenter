import React from "react";

const TopicRow = ({ id, deleteHandler, name }) => {
  return (
    <div className="row">
      <div className="col-8">
        <h6>{name}</h6>
      </div>

      <div className="col-4">
        <i
          className="bi bi-x-circle text-danger "
          onClick={() => {
            deleteHandler(id);
          }}
        />
      </div>
    </div>
  );
};

export default TopicRow;
