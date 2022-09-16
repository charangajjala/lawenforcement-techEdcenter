import React from "react";
import BreadCrumbs from "../../util/components/BreadCrumbs";

const MissionStatement = () => {
  return (
    <div>
      <BreadCrumbs
        list={["Home", "Mission Statement"]}
        title="Mission Statement"
      />
      <div class="container page-body" style={{ textAlign: "justify" }}>
        <div class="row">
          <div class="col-sm-11">
            <h3>POLICE TECHNICAL - Technical. Training. Solutions.</h3>
            <br />
            <p>
              Founded in 2005, POLICE TECHNICAL provides technical training to
              law enforcement (Federal, State and Local) throughout North
              America. We are proud to offer on-demand technical courses, taught
              by active law personnel.
            </p>
          </div>
        </div>
      </div>
      <div className="d-none">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Fuga quasi architecto esse maxime harum dolores unde ea officiis alias dolorem iusto, ab accusamus dicta in, accusantium impedit porro illum iure!</div>
      <div className="d-none">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Fuga quasi architecto esse maxime harum dolores unde ea officiis alias dolorem iusto, ab accusamus dicta in, accusantium impedit porro illum iure!</div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <br />
      <div class="row"></div>
    </div>
  );
};

export default MissionStatement;
