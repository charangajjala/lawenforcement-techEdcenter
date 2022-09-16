import React, { useMemo, useEffect, useState } from "react";
import useInput from "../../hooks/use-input";
import Col from "./Col";
import SelectOne from "./SelectOne";
import { selectStates } from "../../constants/selectConstants";

const Address = ({ init, cb, cbref, mode }) => {
  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [addr1, addr1Handler] = useInput(
    useInputInit(init ? init.address1 : null)
  );
  const [addr2, addr2Handler] = useInput(
    useInputInit(init ? init.address2 : null)
  );
  const [city, cityHandler] = useInput(useInputInit(init ? init.city : null));
  const [state, setState] = useState("");
  const [zip, zipHandler] = useInput(useInputInit(init ? init.zip : null));

  const addrObj = useMemo(() => {
    if (!addr1 && !addr2 && !city && !state && !zip) return null;
    return {
      address1: addr1,
      address2: addr2,
      city,
      zip,
      state,
    };
  }, [addr1, addr2, city, zip, state]);

  useEffect(() => {
    if (addrObj !== undefined) {
      cb(cbref, addrObj);
    }
  }, [cb, addrObj, cbref]);
  console.log("here before", state);

  return (
    <div className="row m-0 p-0">
      <Col
        col="col-12  "
        label="Address1"
        value={addr1}
        onChange={addr1Handler}
        required={false}
      />
      <Col
        col="col-12  "
        label="Address2"
        value={addr2}
        onChange={addr2Handler}
        required={false}
      />
      <Col
        col="col-12 "
        label="City"
        value={city}
        onChange={cityHandler}
        required={false}
      />
      <SelectOne
        col="col-12  "
        selectEntitys={selectStates}
        data={init ? init.state : undefined}
        comp="value"
        val="value"
        show="name"
        title="State"
        cb={setState}
        titlecol="p-0 m-0"
        initTxt="Select State"
        required={false}
      />
      <Col
        col="col-12 "
        label="Zip"
        value={zip}
        onChange={zipHandler}
        required={false}
      />
    </div>
  );
};

export default Address;