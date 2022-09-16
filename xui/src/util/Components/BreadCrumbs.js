import React from "react";
import { Link } from "react-router-dom";

const BreadCrumbs = ({ list, title }) => {
  return (
    <>
      <div className="container ">
        <div className="row ">
          <div className="col-sm-6 pt-2">
            <h2 className="page-title">{title}</h2>
          </div>
          <div className="col-sm-6 d-flex justify-content-end align-self-end">
            <h6 className="m-0">
              <small>
                <nav aria-label="breadcrumb">
                  <ol className="breadcrumb">
                    {list.map((item, i) => {
                      const last = i === list.length - 1;
                      return (
                        <li
                          key={i}
                          className={`breadcrumb-item ${last && "active"}`}
                        >
                          {last ? (
                            item
                          ) : (
                            <Link to={`/${item.toLowerCase()}`}>{item}</Link>
                          )}
                        </li>
                      );
                    })}
                  </ol>
                </nav>
              </small>
            </h6>
          </div>
        </div>
      </div>
      <hr className="mb-3" />
    </>
  );
};

export default BreadCrumbs;
