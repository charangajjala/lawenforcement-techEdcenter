import React from "react";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import image from "../../images/Prospectus_2017_Thumbnail.jpg";
import logo1 from "../../images/Standard-Cut-Out-No-Gradient-300x92.png"
import logo2 from "../../images/Blue-Shield-Title-Black-Tagline-300x92.png"

const CompanyDoc = () => {
  return (
    <div>
      <BreadCrumbs
        list={["Home", "Company Documentation"]}
        title="Company Documentation"
      />
      <div className="container page-body" style={{ textAlign: "justify" }}>
        <div className="row">
          <div className="col-sm-3">
            <a href="#">
              <img
                src={image}
                className="img-fluid img-thumbnail"
                max-width="228px"
                alt="Loading"
              />
            </a>
          </div>
          <div className="col-sm-9">
            <p>
              The following documents are intended for marketing purposes and
              may be duplicated by host agencies in support of Police Technical
              courses. No other users are authorized. For information regarding
              duplication please contact{" "}
              <a href="mailto:info@policetechnical.com">
                info@policetechnical.com
              </a>
              .
            </p>
            <a href="#">2018 POLICE TECHNICAL Prospectus</a>
            <p>
              Prospectus outlines current and new courses, as well as POLICE
              TECHNICAL products and services.
            </p>
            <p>
              This document helps agencies choose the best couses and services
              for their specific needs. Student Evaluations and detailed
              outlines for all services allow agencies to have a clear picture
              of our solutions.
            </p>
          </div>
        </div>

        <hr />

        <div className="row">
          <div className="col-sm">
            <a href="#">POLICE TECHNICAL Courses with Descriptions</a>
          </div>
        </div>
        <div className="row">
          <div className="col-sm">
            <a href="#">POLICE TECHNICAL 2018 W9</a>
          </div>
        </div>
        <div className="row">
          <div className="col-sm">
            <p>CAGE Code: 5F3F5</p>
          </div>
        </div>
        <div className="row">
          <div className="col-sm">
            <p>GSA#: GS07f146DA</p>
          </div>
        </div>
        <div className="row">
          <div className="col-sm">
            <p>EIN/TIN 27-0476643</p>
          </div>
        </div>
        <div className="row">
          <div className="col-sm">
            <p>IN ID# 0136544878</p>
          </div>
        </div>
        <div className="row">
          <div className="col-sm">
            <p>DUNS# 364549431</p>
          </div>
        </div>

        <hr />

        <div className="row">
          <div className="col-sm">
            <strong>
              <p>POLICE TECHNICAL Logos</p>
            </strong>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-4">
            <img
              src={logo1}
              alt="Loading"
            />
          </div>
          <div className="col-sm-4">
            <img
              src={logo2}
              alt="Loading"
            />
          </div>
        </div>
      </div>

      <br />
      <div className="row"></div>
    </div>
  );
};

export default CompanyDoc;
