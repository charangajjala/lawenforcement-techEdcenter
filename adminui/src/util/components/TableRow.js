import React from "react";
import { Link } from "react-router-dom";

const TableRow = ({ data, path, del, order }) => {
  return (
    <tr>
      {order.map((key, i) => {
        if (key === "id" && path === "courses") return null;
        if (key === "createdBy") {
          return (
            <td key={i}>{`${data[key].firstName} ${data[key].lastName}`}</td>
          );
        }
        if (key === "host" || key === "location") {
          return <td key={i}>{data[key] ? String(data[key]) : "TBD"}</td>;
        }
        return <td key={i}>{String(data[key])}</td>;
      })}
      <div>
        <Link
          to={`/${path}/${data.id !== undefined ? data.id : data.invoiceNum}`}
        >
          <button className="btn btn-primary mr-5 ">View</button>
        </Link>

        <Link
          to={`/${path}/${data.id !== undefined ? data.id : data.invoiceNum}`}
        >
          <button className="btn btn-primary mr-5 ">Edit</button>
        </Link>

        <button
          className="btn btn-primary mr-5 "
          onClick={() => del(data.id !== undefined ? data.id : data.invoiceNum)}
        >
          Delete
        </button>
      </div>
    </tr>
  );
};

export default TableRow;
