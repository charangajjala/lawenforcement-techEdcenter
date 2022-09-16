import React from "react";
import BreadCrumbs from "../../util/components/BreadCrumbs";

const History = () => {
  const histories = [
    {
      date: "April 22, 2005",
      description:
        "POLICE TECHNICAL LLC was established to further professionalize the law enforcement training processes created by its founder, Thomas M. Manson.",
    },
    {
      date: "2007",
      description:
        "POLICE TECHNICAL LLC was recognized as a Sole Source Provider by federal law enforcement agencies, offering technical training unavailable from any other source.",
    },
    {
      date: "June 30, 2009",
      description:
        "POLICE TECHNICAL incorporated to provide a suitable structure to expand business operations.  By 2010, POLICE TECHNICAL was scheduling 50 courses a year across North America.",
    },
    {
      date: "2011",
      description:
        "POLICE TECHNICAL made national announcements seeking additional instructors to meet growing requests for technical training among law enforcement.",
    },
    {
      date: "2012",
      description:
        "5 new courses were being taught by additional instructors, each trained in POLICE TECHNICAL instructional methodologies.",
    },
    {
      date: "2014",
      description: `18 POLICE TECHNICAL instructors were providing national level law enforcement training in five distinct, 80 hr certification tracks, including:
    Analytics and Intelligence (AAI),
    Applied Applications (AAP),
    Cell Phone Investigations (CPI),
    Leadership and Technology (LAT),
    Open Source Investigations (OSI)`,
    },
    {
      date: "August 3, 2016",
      description: `POLICE TECHNICAL became GSA Contractor. # GS-07F-146DA
    DUNS: 364549431
    NAICS : 611699`,
    },
    {
      date: "January 11, 2018",
      description: `POLICE TECHNICAL became HUBZone Certified.`,
    },
  ];
  return (
    <div>
      <BreadCrumbs list={["Home", "History"]} title="History" />
      <div className="container">
        {histories.map((history, i) => (
          <div className="row" key={i}>
            {i % 2 === 0 && (
              <>
                <div className="col-sm-6 m-auto">
                  <div className="border rounded p-2 bg-light">
                    <strong className="text-primary">{history.date}</strong>{" "}
                    {history.description}
                  </div>
                </div>
                <div className="col-sm-6"></div>
              </>
            )}
            {i % 2 !== 0 && (
              <>
                <div className="col-sm-6"></div>
                <div className="col-sm-6 m-auto">
                  <div className="border rounded p-2 bg-light">
                    <strong className="text-primary">{history.date}</strong>{" "}
                    {history.description}
                  </div>
                </div>
              </>
            )}
          </div>
        ))}
      </div>

      <br />
      <div className="row"></div>
    </div>
  );
};

export default History;
