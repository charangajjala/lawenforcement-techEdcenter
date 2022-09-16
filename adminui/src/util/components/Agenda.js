import React, { useEffect, useState, useCallback } from "react";
import Desc from "./Desc";

const Agenda = ({ value, dayNum, cb ,required}) => {
  const [agendaObj, setAgendaObj] = useState({});

  const giveData = useCallback(
    (dayAgendaObj) => {
      setAgendaObj({ day: dayNum, value: dayAgendaObj });
    },
    [dayNum]
  );

  useEffect(() => {
    if (agendaObj) {
      cb(agendaObj);
    }
  }, [agendaObj, cb]);

  return (
    <div className="col-md-4">
      <div className="text-center">
        <h5 className="m-0 p-0">{`Day ${dayNum}`}</h5>
      </div>
      <h6 className="p-0 m-0">Value</h6>
      <Desc col="row overflow-auto" cb={giveData} descData={value} required={required} />
    </div>
  );
};

export default Agenda;
