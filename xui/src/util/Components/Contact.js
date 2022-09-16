import React, { useEffect, useMemo } from "react";
import useInput from "../../hooks/use-input";
import Col from "./Col";

const Contact = ({ init, cb, cbref, mode }) => {
  const useInputInit = (initval) => (mode === "EDIT" ? initval : null);
  const [title, titleHandler] = useInput(
    useInputInit(init ? init.title : null)
  );
  const [name, nameHandler] = useInput(useInputInit(init ? init.name : null));
  const [email, emailHandler] = useInput(
    useInputInit(init ? init.email : null)
  );
  const [phone, phoneHandler] = useInput(
    useInputInit(init ? init.phone : null)
  );
  const [email2, email2Handler] = useInput(
    useInputInit(init ? init.email2 : null)
  );
  const [phone2, phone2Handler] = useInput(
    useInputInit(init ? init.phone2 : null)
  );

  const contactObj = useMemo(() => {
    if (!title && !name && !email && !phone && !email2 && !phone2) return null;
    return {
      name,
      email,
      phone,
      email2,
      phone2,
      title,
    };
  }, [email, phone, phone2, name, email2, title]);

  useEffect(() => {
    if (contactObj !== undefined) {
      cb(cbref, contactObj);
    }
  }, [cb, cbref, contactObj]);

  return (
    <div className="row p-0 m-0">
      <Col
        col="col-12  "
        label="Title"
        value={title}
        onChange={titleHandler}
        required={false}
      />
      <Col
        col="col-12  "
        label="Name"
        value={name}
        onChange={nameHandler}
        required={false}
      />
      <Col
        col="col-12 "
        label="Email"
        value={email}
        onChange={emailHandler}
        required={false}
      />
      <Col
        col="col-12 "
        label="Phone"
        value={phone}
        onChange={phoneHandler}
        required={false}
      />
      <Col
        col="col-12 "
        label="Email2"
        value={email2}
        onChange={email2Handler}
        required={false}
      />
      <Col
        col="col-12 "
        label="Phone2"
        value={phone2}
        onChange={phone2Handler}
        required={false}
      />
    </div>
  );
};

export default Contact;

