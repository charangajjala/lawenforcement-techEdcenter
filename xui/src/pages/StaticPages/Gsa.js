import React from "react";
import BreadCrumbs from "../../util/components/BreadCrumbs";
import gsa1 from "../../images/200-gsa.png";
import gsa2 from "../../images/207sba.png";
import gsa3 from "../../images/200-hubzone.png";

const Gsa = () => {
  return (
    <div>
      <BreadCrumbs list={["Home", "GSA"]} title="GSA" />
      <div className="container ">
        <div className="row">
          <div className="col">
            <p>
              Founded in 2005, POLICE TECHNICAL was awarded a GSA Contract,
              GS-07F-146DA, August 3, 2016. POLICE TECHNICAL provides technical
              training to law enforcement (Federal, State and Local) throughout
              North America. We are proud to offer on-demand technical courses,
              taught by active law personnel and qualified trade professionals.
            </p>
            <br />
          </div>
        </div>
        <div className="row">
          <div className="col-sm-4">
            <div className="row" style={{ justifyContent: "center" }}>
              <img src={gsa1} alt="gsa" />
            </div>
          </div>
          <div className="col-sm-4">
            <div className="row" style={{ justifyContent: "center" }}>
              <img src={gsa2} alt="sba" />
            </div>
          </div>
          <div className="col-sm-4">
            <div className="row" style={{ justifyContent: "center" }}>
              <img src={gsa3} alt="hubzone" />
            </div>
          </div>
        </div>

        <div
          className="container-fluid"
          style={{ backgroundColor: "#0070C0" }}
        ></div>

        <div className="container">
          <div id="parent">
            <div className="card my-2">
              <div className="card-header">
                <a
                  className="card-link"
                  data-toggle="collapse"
                  href="#codes-classifications"
                >
                  Codes and Classifications
                </a>
              </div>
              <div
                id="codes-classifications"
                className="collapse show"
                data-parent="#parent"
              >
                <div className="card-body">
                  <div className="row">
                    <div className="col-sm-6">
                      <p>
                        <strong>NAICS:</strong>
                      </p>
                      <p>
                        611430 Professional and Management Development Training
                        <br />
                        611420 Computer Training
                        <br />
                        611699 All other Miscellaneous Schools and Instruction
                        <br />
                        611519 Other Technical and Trade Schools
                        <br />
                        922120 Police Protection
                      </p>
                    </div>
                    <div className="col-sm-6">
                      <br />
                      <table className="table table-sm table-borderless">
                        <tbody>
                          <tr>
                            <th>CAGE Code:</th>
                            <td>5F3F5</td>
                          </tr>
                          <tr>
                            <th>GSA#:</th>
                            <td>GS07F146DA</td>
                          </tr>
                          <tr>
                            <th>EIN/TIN:</th>
                            <td>27-0476643</td>
                          </tr>
                          <tr>
                            <th>DUNS#:</th>
                            <td>364549431</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div className="row">
                    <div className="col-sm-12">
                      <p>
                        <strong>Federal Supply Schedule: 84</strong>
                        <br />
                        Total Solutions for Law Enforcement, Security,
                        Facilities Management, Fire...
                      </p>
                      <p>
                        <strong>Category: 426 6</strong>
                        <br />
                        Law Enforcement and Security Training
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="card my-2">
              <div className="card-header">
                <a
                  className="card-link"
                  data-toggle="collapse"
                  href="#core-competencies"
                >
                  Core Competencies
                </a>
              </div>
              <div
                id="core-competencies"
                className="collapse"
                data-parent="#parent"
              >
                <div className="card-body">
                  <div className="row" style={{ justifyContent: "center" }}>
                    <p>
                      POLICE TECHNICAL has nationally recognized Core
                      Competencies in providing the following services
                    </p>
                  </div>
                  <div className="row">
                    <div className="col-sm-12">
                      <table className="table table-sm table-borderless">
                        <tr>
                          <th>Full Lifecycle Technical Training</th>
                        </tr>
                        <tr>
                          <td>
                            Instructor Hiring and Scheduling, Course
                            Development, Online Student Registrations, Tracking
                            and Certifications, Course Materials, Instructor
                            Development, Evaluations, After Action Review, and
                            Financial Accountability.
                          </td>
                        </tr>
                        <tr>
                          <th>Proprietary Training Software Design</th>
                        </tr>
                        <tr>
                          <td>
                            Internally developed web based software, which has
                            processed 10s of thousands of law enforcement,
                            military and private contractors registrations for
                            multiple international companies.
                          </td>
                        </tr>
                        <tr>
                          <th>
                            Certification Training in the following areas:
                          </th>
                        </tr>
                        <tr>
                          <td>
                            Analytics and Intelligence, Applied Applications
                            (i.e Microsoft), Cell Phone Investigation,
                            Leadership and Technology, Open Source
                            Investigations, PIO and Community Engagements.
                          </td>
                        </tr>
                        <tr>
                          <th>Customized Training:</th>
                        </tr>
                        <tr>
                          <td>
                            Fully customizable programs for Public (Law
                            Enforcement and Intelligence at all levels) and
                            Private (Fortune 500) clients.
                          </td>
                        </tr>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="card my-2">
              <div className="card-header">
                <a
                  className="card-link"
                  data-toggle="collapse"
                  href="#past-performance"
                >
                  Past Performance
                </a>
              </div>
              <div
                id="past-performance"
                className="collapse"
                data-parent="#parent"
              >
                <div className="card-body">
                  <div className="row">
                    <div className="col-sm-12">
                      <table className="table table-sm table-borderless">
                        <tr>
                          <td>Appalaichia HIDTA</td>
                        </tr>
                        <tr>
                          <td>Arizona HIDTA</td>
                        </tr>
                        <tr>
                          <td>
                            Bureau of Alcohol, Tobacco, Firearms and Explosives
                            (ATF)
                          </td>
                        </tr>
                        <tr>
                          <td>California DOJ</td>
                        </tr>
                        <tr>
                          <td>California POST</td>
                        </tr>
                        <tr>
                          <td>Drug Enforcement Administration (DEA)</td>
                        </tr>
                        <tr>
                          <td>Federal Bureau of Investigation (FBI)</td>
                        </tr>
                        <tr>
                          <td>Georgia Bureau of Investigation</td>
                        </tr>
                        <tr>
                          <td>Harris County Sheriff's Office</td>
                        </tr>
                        <tr>
                          <td>Houston HIDTA</td>
                        </tr>
                        <tr>
                          <td>National Guard Counterdrug Program</td>
                        </tr>
                        <tr>
                          <td>New Mexico HIDTA</td>
                        </tr>
                        <tr>
                          <td>Northern California HIDTA</td>
                        </tr>
                        <tr>
                          <td>NYPD</td>
                        </tr>
                        <tr>
                          <td>Oregon-Idaho HIDTA</td>
                        </tr>
                        <tr>
                          <td>PR/USVI HIDTA</td>
                        </tr>
                        <tr>
                          <td>Rocky Mountain Information Network (RMIN)</td>
                        </tr>
                        <tr>
                          <td>Washington/Baltimore HIDTA</td>
                        </tr>
                        <tr>
                          <td>West Texas HIDTA</td>
                        </tr>
                        <tr>
                          <td>Western States Information Network (WSIN)</td>
                        </tr>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <br />
        <h5>Terms and Conditions</h5>
        
        <h5 className="mt-2">Capability Statement</h5>
        <a href="https://www.policetechnical.com/wp-content/uploads/2021/08/CapabilityStatement2021.pptx">CapabilityStatement2022</a>
        
        <div className="row"></div>
      </div>
    </div>
  );
};

export default Gsa;
