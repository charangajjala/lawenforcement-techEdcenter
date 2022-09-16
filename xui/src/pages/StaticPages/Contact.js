import React, { useRef } from "react";
import useHttp from "../../hooks/use-http";
import useAlert from "../../hooks/use-alert";
import SetAlert from "../../util/components/SetAlert";
import BreadCrumbs from "../../util/components/BreadCrumbs";

const Contact = () => {
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const name = useRef();
  const email = useRef();
  const message = useRef();
  const subject = useRef();

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("contact send");
    try {
      await sendRequest(
        {
          url: "/contact/",
          method: "POST",
          body: {
            name: name.current.value,
            email: email.current.value,
            message: message.current.value,
            subject: subject.current.value,
          },
        },
        null
      );
      setShowAlert(true);
      setAlertMessage("Message sent successfully!");
    } catch (error) {}
  };

  return (
    <div>
      <BreadCrumbs list={["Home", "Contact"]} title="Contact" />
      <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
      <div className="container">
        <p>
          To reach POLICE TECHNICAL via email please fill out the fields below.
          Once submitted, you’ll receive a prompt reply. We can also be reached
          by phone at 812-232-4200.
        </p>
        <br />

        <div className="row">
          <div className="col-sm-7">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <input
                  type="text"
                  className="form-control my-2"
                  name="name"
                  placeholder="Name"
                  required
                  ref={name}
                />
                <input
                  type="email"
                  className="form-control my-2"
                  name="email"
                  placeholder="Email"
                  required
                  ref={email}
                />
                <input
                  type="text"
                  className="form-control my-2"
                  name="subject"
                  placeholder="Subject"
                  required
                  ref={subject}
                />
                <textarea
                  name="message"
                  rows="6"
                  className="form-control my-2"
                  placeholder="Message"
                  required
                  ref={message}
                ></textarea>
              </div>
              <div className="row form-group align-content-center m-0 p-0 ">
                <div className="col-sm-4 ">
                  {" "}
                  <input
                    type="submit"
                    className="btn btn-success"
                    value="Submit"
                  />
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
