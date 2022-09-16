import React, { useState, useRef, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import FilterInput from "../util/components/FilterInput";
import { selectStates } from "../constants/selectConstants";
import { useParams } from "react-router-dom";
import useHttp from "../hooks/use-http";
import SetAlert from "../util/components/SetAlert";
import useAlert from "../hooks/use-alert";
import BreadCrumbs from "../util/components/BreadCrumbs";

const CheckOutPage = ({ invoice, clsid }) => {
  const list = ["Home", "Checkout"];
  return (
    <div>
      <BreadCrumbs list={list} title="CheckOut" />
      <div class="container">
        <p>
          <strong>Thank you for registering with POLICETECHNICAL!</strong>
        </p>
        <br />

        <p>
          Emails with their account and class information have been sent to the
          attendee(s).
        </p>
        <p>
          A confirmation email along with invoice details has been sent to{" "}
          <strong>{invoice.pmremail}</strong>.
        </p>
        <p>
          You may also access the same from{" "}
          <Link
            to={`/invoice/${clsid}/${invoice.invoiceNum}/${invoice.accessKey}`}
          >
            here
          </Link>
        </p>

        <p>Invoice no. {invoice.invoiceNum}</p>
      </div>

      <br />
      <div class="row"></div>
    </div>
  );
};

const CheckoutForm = ({
  cls,
  course,
  location,
  activate,
  setCollect,
  give,
  numStudents,
}) => {
  const [type, setType] = useState("");
  const [promoInvalid, setPromoInvalid] = useState(false);
  const nameoncard = useRef({ value: "" });
  const cardnumber = useRef({ value: "" });
  const expirydate = useRef({ value: "" });
  const cvv = useRef({ value: "" });
  const promoCode = useRef({ value: "" });
  const [sendRequest] = useHttp();
  const changePayType = (e) => {
    setType(e.target.value);
  };
  const [discount, setDiscount] = useState({ apply: false });

  const applyPromo = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const applyPromo = (res) => {
        setDiscount((prev) => {
          prev.apply = true;
          const { type, value } = res;
          let discount = 0;
          if (type === "Seats") {
            discount = parseFloat(value) * parseFloat(cls.fee);
          } else if (type === "Flat") {
            discount = parseFloat(value);
          } else {
            discount = (parseFloat(cls.fee) * parseFloat(value)) / 100;
          }
          return { ...prev, ...res, discount };
        });
      };
      if (promoCode.current.value !== "")
        await sendRequest(
          { url: `promos/${promoCode.current.value}/` },
          applyPromo
        );
    } catch (error) {
      setPromoInvalid(true);
      setDiscount({ apply: false });
      setTimeout(() => {
        setPromoInvalid(false);
      }, 3000);
    }
  };

  const discountJsx = () => {
    if (discount.apply) {
      let jsx = "Applied Successfully ";
      const { type, value, discount: amount } = discount;
      if (type === "Seats") {
        jsx = jsx + `${value} Seats off ($${amount} off)`;
      } else if (type === "Flat") {
        jsx = jsx + `Flat $${value} off`;
      } else {
        jsx = jsx + `${value}% off ($${amount} off)`;
      }
      return <h6 className="text-success">{jsx}</h6>;
    }
  };

  const price = discount.apply
    ? parseFloat(cls.fee) * numStudents - discount.discount >= 0
      ? parseFloat(cls.fee) * numStudents - discount.discount
      : 0
    : parseFloat(cls.fee) * numStudents;

  const checkoutSubmit = (e) => {
    e.preventDefault();
    e.stopPropagation();
    give({
      paymentMethod: type,
      promoId: discount.id,
      price,
    });
    console.log("setting collect to true");
    setCollect({ collect: true });
  };
  return (
    activate === "paymentform" && (
      <>
        <p>
          <strong>{course.title}</strong>
          <br />
          {cls.startDate} - {cls.endDate}
          <br />
          {location.name || ""}
        </p>

        <table className="table-sm table-borderless" id="register-summary">
          <tr>
            <th>Fee</th>
            <th className="float-right">Attendees</th>
          </tr>
          <tr>
            <td>{"$" + cls.fee}</td>
            <td className="float-right">
              <span id="quantity">{numStudents}</span>
            </td>
          </tr>
          <tr>
            <td></td>
          </tr>
          <tr>
            <td>
              <form onSubmit={applyPromo}>
                <FilterInput
                  label="Promo Code"
                  filtref={promoCode}
                  col="d-inline"
                />
                {!!promoInvalid && (
                  <h6 className="text-danger">Promocode is Invalid</h6>
                )}
                {discountJsx()}
                <input
                  type="submit"
                  className="btn btn-primary"
                  value="Apply"
                />
              </form>
            </td>
          </tr>

          <tr>
            <th>Total:</th>
            <th className="float-right">{`${price + "$"}`}</th>
          </tr>
        </table>
        <br />

        <p>
          <strong>Choose a Payment Type: </strong>
        </p>
        <form onSubmit={checkoutSubmit}>
          <div className="form-group">
            <select
              className="form-select"
              required
              onChange={changePayType}
              value={type}
            >
              <option value="" disabled defaultValue>
                Payment Type
              </option>

              <option value="Credit Card">Credit Card</option>
              <option value="Pay Later">Pay Later</option>
            </select>
          </div>

          {type === "Credit Card" && (
            <div className="form-group" id="payment-cc">
              <FilterInput
                label="Name on Card"
                required={true}
                filtref={nameoncard}
              />
              <FilterInput
                label="Card Number"
                required={true}
                filtref={cardnumber}
              />
              <FilterInput
                label="Expiration Date (MMYY)"
                required={true}
                filtref={expirydate}
              />
              <FilterInput label="CVV" required={true} filtref={cvv} />
            </div>
          )}

          <br />

          <div className="form-group">
            <input
              className="btn btn-success"
              type="submit"
              value="Check Out"
            />
          </div>
        </form>
      </>
    )
  );
};

const RegisterForm = ({
  isAtndee,
  activate,
  setActivate,
  onEmailBlur,
  foundStudent,
  giveNoStudents,
  collect,
  give,
}) => {
  const [students, setStudents] = useState([]);
  const [pmr, setPmr] = useState({});
  const [disableStudentAdd, setDisableStudentAdd] = useState(false);

  useEffect(() => {
    if (foundStudent !== undefined && foundStudent.studentId !== undefined) {
      setStudents((prev) => {
        const existing = prev.find(
          (s) => s.studentId === foundStudent.studentId
        );
        if (existing) return prev;
        return [...prev, foundStudent];
      });
      setEntity();
    }
  }, [foundStudent]);

  useEffect(() => {
    if (isAtndee) giveNoStudents(students.length);
  }, [giveNoStudents, isAtndee, students]);

  useEffect(() => {
    if (collect) {
      if (isAtndee) {
        give(
          students.map((s) => {
            if (s.studentId) {
              return s.studentId;
            }
            return s;
          })
        );
      }
    } else {
      give(pmr);
    }
  }, [collect, give, isAtndee, students, pmr]);

  const title = useRef({ value: "" });
  const email = useRef({ value: "" });
  const email2 = useRef({ value: "" });
  const name = useRef({ value: "" });
  const firstName = useRef({ value: "" });
  const lastName = useRef({ value: "" });
  const phone = useRef({ value: "" });
  const address = useRef({ value: "" });
  const address2 = useRef({ value: "" });
  const city = useRef({ value: "" });
  const state = useRef({ value: "" });
  const zip = useRef({ value: "" });
  const agency = useRef({ value: "" });

  const constructEntity = () => {
    return {
      email: email.current.value,
      firstName: firstName.current.value,
      lastName: lastName.current.value,
      phone: phone.current.value,
      address: address.current.value,
      city: city.current.value,
      state: state.current.value,
      zip: zip.current.value,
      agency: agency.current.value,
      title: title.current.value,
      name: name.current.value,
      email2: email2.current.value,
      address2: address2.current.value,
    };
  };
  const setEntity = (entity) => {
    email.current.value = entity ? entity.email : "";
    firstName.current.value = entity ? entity.firstName : "";
    lastName.current.value = entity ? entity.lastName : "";
    phone.current.value = entity ? entity.phone : "";
    address.current.value = entity ? entity.address : "";
    city.current.value = entity ? entity.city : "";
    state.current.value = entity ? entity.state : "";
    zip.current.value = entity ? entity.zip : "";
    agency.current.value = entity ? entity.agency : "";
    title.current.value = entity ? entity.title : "";
    name.current.value = entity ? entity.name : "";
    email2.current.value = entity ? entity.email2 : "";
    address2.current.value = entity ? entity.address2 : "";
  };

  const addStudent = (e) => {
    e.preventDefault();
    const entity = constructEntity();
    setStudents((prevStudents) => {
      prevStudents.filter((s) => s.edit === true);
      return [...prevStudents, entity];
    });
    setEntity();
  };

  const editStudent = (stdnt) => {
    setEntity(stdnt);

    setActivate("studentform");
    setStudents((prevStudents) => {
      prevStudents.find((s) => s.email === stdnt.email).edit = true;
      return [...prevStudents];
    });
  };
  const removeStudent = (stdnt) => {
    setStudents(students.filter((s) => s.email !== stdnt.email));
  };

  const next = (e) => {
    if (activate === "studentform") {
      setActivate("pmrform");
      setStudents((prevStudents) =>
        prevStudents.map((s) => {
          s.edit = false;
          return s;
        })
      );
    } else {
      if (e) e.preventDefault();
      setPmr(constructEntity());
      setActivate("paymentform");
    }
  };

  const addAttendee = () => {
    setActivate("studentform");
  };

  const editPmr = (pmr) => {
    setEntity(pmr);

    setActivate("pmrform");
  };

  if (pmr.email) {
    setEntity(pmr);
    console.log(email.current.value);
  }

  const showForm =
    (isAtndee && activate === "studentform") ||
    (!isAtndee && activate === "pmrform");

  return (
    <>
      {showForm && (
        <form onSubmit={isAtndee ? addStudent : next}>
          <div className="form-group">
            <FilterInput label="Title" filtref={title} col="mb-1" />
            {!isAtndee && (
              <FilterInput
                label="Name"
                required={true}
                filtref={name}
                col="mb-1"
              />
            )}
            <FilterInput
              type="email"
              label="Email"
              required={true}
              filtref={email}
              onBlur={(e) => {
                onEmailBlur(e, students, setDisableStudentAdd);
              }}
              col="mb-1"
            />
            {!isAtndee && (
              <FilterInput
                label="Alternate Email"
                filtref={email2}
                col="mb-1"
              />
            )}
            <FilterInput
              label="First Name"
              required={true}
              filtref={firstName}
              col="mb-1"
            />
            <FilterInput
              label="Last Name"
              required={true}
              filtref={lastName}
              col="mb-1"
            />
            <FilterInput
              label="Phone"
              required={true}
              filtref={phone}
              col="mb-1"
            />
            <FilterInput
              label="Agency"
              required={true}
              filtref={agency}
              col="mb-1"
            />
            <FilterInput
              label="Address1"
              required={true}
              filtref={address}
              col="mb-1"
            />
            <FilterInput
              label="Address2"
              filtref={address2}
              col="mb-1"
            />
            <FilterInput
              label="City"
              required={true}
              filtref={city}
              col="mb-1"
            />
            <FilterInput
              label="State"
              required={true}
              filtref={state}
              options={selectStates}
              show="name"
              val="value"
              col="mb-1"
            />
            <FilterInput label="ZIP" required={true} filtref={zip} />
          </div>
          <br />
          <div className="form-group">
            {isAtndee !== false && activate === "studentform" && (
              <input
                className="btn btn-primary "
                type="submit"
                value="Add Another Attendee"
                disabled={disableStudentAdd}
              />
            )}
            {isAtndee === true && (
              <input
                type="button"
                className="btn btn-success mx-1"
                value="Next"
                disabled={students.length === 0 ? true : false}
                onClick={next}
              />
            )}
            {isAtndee === false && (
              <input className="btn btn-success" value="Next" type="submit" />
            )}
          </div>
        </form>
      )}

      {isAtndee === true && (
        <>
          <table className="table-sm table-borderless table-striped">
            {students.map(
              (student, i) =>
                student.edit !== true && (
                  <tr key={i}>
                    <td>
                      {`${student.firstName} ${student.lastName}`}
                      <br />
                      <small> {student.email} </small>
                    </td>
                    <td>
                      <i
                        className="bi bi-pencil"
                        data-toggle="tooltip"
                        title="Edit"
                        onClick={() => {
                          editStudent(student);
                        }}
                      ></i>
                      <i
                        className="bi bi-trash"
                        onClick={() => {
                          removeStudent(student);
                        }}
                        data-toggle="tooltip"
                        title="Remove"
                      ></i>
                    </td>
                  </tr>
                )
            )}
          </table>
          <br />
        </>
      )}
      {isAtndee === true && activate !== "studentform" && (
        <button className="btn btn-primary" onClick={addAttendee}>
          Add Attendee
        </button>
      )}
      {pmr.email && activate !== "pmrform" && (
        <div>
          <strong>{`${pmr.firstName} ${pmr.lastName}`}</strong> <br />
          <span>{pmr.email}</span>
          <br />
          <span>{pmr.agency}</span>F
          <br />
          <span>{pmr.address}</span>
          <br />
          <span>{pmr.city + ", " + pmr.state + " " + pmr.zip}</span>
          <br />
          <span>{pmr.phone}</span>
          <br />
        </div>
      )}
      {isAtndee === false && activate !== "pmrform" && pmr.email !== undefined && (
        <button
          className="btn btn-primary"
          onClick={() => {
            editPmr(pmr);
          }}
        >
          Edit
        </button>
      )}
    </>
  );
};

const ClassRegisterPage = () => {
  const [activate, setActivate] = useState("studentform");
  const [showAlert, setShowAlert, alertMessage, setAlertMessage] = useAlert();
  const [sendRequest] = useHttp(setAlertMessage, setShowAlert);
  const [cls, setClass] = useState({});
  const [course, setCourse] = useState({});

  const params = useParams();

  const [foundStudent, setFoundStudent] = useState({});
  const [collect, setCollect] = useState({ collect: false });
  const numStudents = useRef(0);
  const newRegistration = useRef({});
  const [showCheckout, setShowCheckout] = useState(false);
  const [invoice, setInvoice] = useState({});

  const list = ["Home", "Regsiter"];

  const getNoStudents = useCallback((num) => {
    numStudents.current = num;
  }, []);

  const location = cls.location || {};

  useEffect(() => {
    sendRequest({ url: `/classes/${params.id}` }, setClass).catch((e) => {});
  }, [params.id, sendRequest]);

  useEffect(() => {
    async function fetch() {
      try {
        await sendRequest({ url: `/courses/${cls.course}` }, setCourse);
      } catch (error) {}
    }
    if (cls.id) fetch();
  }, [params.id, sendRequest, cls]);

  const onEmailBlur = async (e, students, setDisableStudentAdd) => {
    const checkemail = e.target.value;
    const check = students.find((student) => student.email === checkemail);
    if (check) {
      setAlertMessage({
        e: true,
        message: "Student with this email has already been added",
      });
      setShowAlert(true);
      setDisableStudentAdd(true);
      return;
    }
    if (!check) {
      setDisableStudentAdd(false);
    }
    if (checkemail.includes("@")) {
      // unique email check

      const verifyStatus = (res) => {
        if (res.studentId) {
          if (res.alreadyRegistered) {
            setAlertMessage({
              e: true,
              message:
                "Student is already registered for this class.Cannot register again",
            });
            setShowAlert(true);
          } else {
            window.alert(
              `We found a student with this email. 
Email : ${res.email} FirstName : ${res.firstName} LastName : ${res.lastName}`
            );
            setFoundStudent(res);
          }
        }
      };
      try {
        await sendRequest(
          {
            url: `/classes/register/verifyAttendee/${params.id}`,
            body: { email: checkemail },
            method: "POST",
          },
          verifyStatus,
          false
        );
      } catch (error) {}
    }
  };

  const formGiveData = useCallback((data) => {
    if (Array.isArray(data)) {
      newRegistration.current.attendees = data.map((student) => {
        delete student["email2"];
        delete student["name"];
        return student;
      });
    } else {
      newRegistration.current.pmrAgency = data.agency;
      newRegistration.current.pmrAddress = {
        address1: data.address,
        address2: data.address2,
        city: data.city,
        state: data.state,
        zip: data.zip,
      };
      newRegistration.current.pmrContact = {
        title: data.title,
        name: `${data.firstName} ${data.lastName}`,
        email: data.email,
        phone: data.phone,
      };
    }
    setCollect({ collect: true });
  }, []);

  const paymentGiveData = (data) => {
    newRegistration.current.paymentMethod = data.paymentMethod;
    newRegistration.current.totalPrice = data.price;
    newRegistration.current.promoId = data.promoId;
  };

  const checkout = (res) => {
    setShowCheckout(true);
    setInvoice({
      invoiceNum: res.invoiceNum,
      pmremail: newRegistration.current.pmrContact.email,
      accessKey: res.accessKey,
    });
  };

  useEffect(() => {
    const newData = newRegistration.current;
    const post = async () => {
      try {
        console.log("final", newData);
        await sendRequest(
          { url: `/classes/register/${cls.id}`, method: "POST", body: newData },
          checkout
        );
      } catch (error) {
        setCollect({ collect: false });
      }
    };
    if (
      collect.collect &&
      newData &&
      newData.attendees &&
      newData.pmrAgency &&
      newData.paymentMethod
    ) {
      post();
    }
  }, [collect, cls.id, sendRequest]);

  return (
    <>
      {showCheckout === true ? (
        <CheckOutPage invoice={invoice} clsid={cls.id} />
      ) : (
        <>
          <BreadCrumbs list={list} title="Register" />
          <SetAlert alertMessage={alertMessage} showAlert={showAlert} />
          <div className="container">
            <div className="row">
              <div className="col-sm-4">
                <div className="progress  ">
                  <div
                    className="progress-bar  "
                    style={{
                      width: activate === "studentform" ? "100%" : "0%",
                    }}
                  >
                    <span className="progress-text ">Attendees</span>
                  </div>
                </div>
                <br />
                <RegisterForm
                  isAtndee={true}
                  activate={activate}
                  setActivate={setActivate}
                  onEmailBlur={onEmailBlur}
                  foundStudent={foundStudent}
                  giveNoStudents={getNoStudents}
                  give={formGiveData}
                  collect={collect.collect}
                />
              </div>
              <div className="col-sm-4">
                <div className="progress">
                  <div
                    className="progress-bar"
                    id="pmr-progress"
                    style={{ width: activate === "pmrform" ? "100%" : "0%" }}
                  >
                    <span className="progress-text">
                      Person Making Registration
                    </span>
                  </div>
                </div>
                <br />
                <RegisterForm
                  isAtndee={false}
                  activate={activate}
                  setActivate={setActivate}
                  give={formGiveData}
                />
                <br />
              </div>
              <div className="col-sm-4">
                <div className="progress">
                  <div
                    className="progress-bar"
                    id="checkout-progress"
                    style={{
                      width: activate === "paymentform" ? "100%" : "0%",
                    }}
                  >
                    <span className="progress-text">Payment</span>
                  </div>
                </div>
                <br />
                <CheckoutForm
                  cls={cls}
                  course={course}
                  location={location}
                  activate={activate}
                  numStudents={numStudents.current}
                  setCollect={setCollect}
                  give={paymentGiveData}
                />
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default ClassRegisterPage;
