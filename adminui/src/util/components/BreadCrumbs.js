import React from "react";
import { Link } from "react-router-dom";

const BreadCrumbs = ({ list, addEntity, addBtnName, mode }) => {
  const brd = (
    <nav aria-label="breadcrumb">
      <ol className="breadcrumb mb-3">
        {list.map((item, i) => {
          const last = i === list.length - 1;
          return (
            <li key={i} className={`breadcrumb-item ${last && "active"}`}>
              {last ? (
                mode ? (
                  item.name
                ) : (
                  item
                )
              ) : (
                <Link to={mode ? item.path : `/${item.toLowerCase()}`}>
                  {mode ? item.name : item}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );

  return (
    <>
      {!addEntity && brd}
      {addEntity && (
        <div className="row mb-3">
          <div className="col-10">{brd}</div>
          <div className="col-2">
            <Link to={`/${addEntity}`}>
              <button type="button" className="btn btn-dark ">
                {`Add ${addBtnName || addEntity.toUpperCase()}`}
              </button>
            </Link>
          </div>
        </div>
      )}
    </>
  );
};

export default BreadCrumbs;
