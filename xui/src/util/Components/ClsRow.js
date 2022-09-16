import React from "react";

const ClsRow = ({ name, val }) => {
  return (
    <tr>
      <th className="table-active ">{name}</th>
      <td>{val}</td>
    </tr>
  );
};

export default ClsRow;
