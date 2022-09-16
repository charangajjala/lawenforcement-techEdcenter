import React from "react";
import BreadCrumbs from "../../util/components/BreadCrumbs";

const Faq = () => {
  const faqs = [
    {
      id: 1,
      question: "Accessing your classes course materials",
      answer: (
        <ul>
          <li>
            To access the course materials for one of your classes, you must be
            signed in and on your <a href="/userprofile/">profile page</a>
          </li>
          <li>
            Click on the&nbsp;<strong>Course Materials&nbsp;</strong>tab
          </li>
          <li>
            Under this tab is a drop down box with each course and their
            materials
          </li>
          <li>
            To gain access to download the listed course materials you must have
            completed a class, or attended a conference under that course
          </li>
          <li>
            If one of these are true, you will gain access to download the
            course materials listed
          </li>
        </ul>
      ),
    },
    {
      id: 2,
      question: "Completing your Class Evaluation and Downloading your Certificate",
      answer: (
        <ul>
          <li>
            To complete your class evaluation and download your certificate, you
            must login to your account and visit your profile from the&nbsp;
            <strong>
              <a href="/userprofile/">View Profile</a>
            </strong>{" "}
            tab at the top of the Police Technical website.
          </li>
          <li>
            Under your profile you will see a tab titled&nbsp;
            <strong>Past Classes.&nbsp;</strong>This contains a list of all your
            previously attended classes.
          </li>
          <li>
            Under each class you will see a link next to&nbsp;
            <strong>Download certificate.</strong>
          </li>
          <li>
            If you have not yet completed your class evaluation, you will be
            prompted to do so. After which, you will be redirect to a download
            page for your class certificate.{" "}
            <em>
              You may revisit this page at any time to re-download your
              certificate.
            </em>
          </li>
        </ul>
      ),
    },
    {
      id: 3,
      question: "Gaining access to community",
      answer: (
        <ul>
          <li>
            Community is a forum strictly limited to law enforcement personnel.
            To gain access to this forum, you must become a verified&nbsp;user
            with Police Technical
          </li>
          <li>
            <strong>The first way</strong>&nbsp;to become a verified user is to
            register and complete a class with Police Technical. Once the class
            has been closed, you will gain access to all of the forum topics
          </li>
          <li>
            <strong>The second way</strong> to become a verified user is to
            register as a user, and request your account be verified.
          </li>
          <li>
            At the top of the Police Technical website, you will see a&nbsp;
            <strong>Register&nbsp;</strong>tab
          </li>
          <li>
            On this page, you will be prompted to create an account. Be sure to
            complete the form with accurate data in order for us to verify that
            you are law enforcement personnel
          </li>
          <li>
            Once your form has been submitted, your account will be created.{" "}
            <em>
              <strong>
                Be sure to verfiy your email address withing 24 hours.
              </strong>
            </em>
          </li>
          <li>
            You will have limited access to the “General” forums on community
            until a Police Technical representative has verified your account
            information. You will receive an email within 24 hours if your
            account information has been verified as being law enforcement
            personnel
          </li>
        </ul>
      ),
    },
    {
      id: 4,
      question: "Hosting a Police Technical class",
      answer: (
        <ul>
          <li>
            This first step to hosting a Police Technical class is to register
            as a pending host. This can be done from the&nbsp;
            <strong>
              <a href="/hostprofileadd/">Become a Host</a>
            </strong>{" "}
            tab under the main navigation bar: Services &gt; Training &gt;{" "}
            <a href="/hostprofileadd/">Become a Host</a>
          </li>
          <li>
            Complete the available form with&nbsp;accurate information and
            click&nbsp;<strong>Submit Sponsor Form&nbsp;</strong> at the bottom
            of the page
          </li>
          <li>
            After successfully submitting the form, you will receive an email
            containing the login credentials for your host profile
          </li>
          <li>
            This account will allow you to change your host information, contact
            Police Technical directly, view an exclusive news feed for hosts,
            and view current and past classes upon becoming an active host
          </li>
          <li>
            A Police Technical representative will look over your
            account&nbsp;information and get back to you regarding the status of
            your account and further actions to be completed
          </li>
        </ul>
      ),
    },
    {
      id: 5,
      question: "Publishing a book with Police Technical",
      answer: (
        <ul>
          <li>
            To begin the process of publishing a book through Police Technical,
            you must first register as an author under the&nbsp;
            <strong>
              <a href="/become-an-author/">Get Published</a>&nbsp;
            </strong>
            link under the main navigation bar: Services &gt; Publishing &gt;{" "}
            <a href="/become-an-author/">Get Published</a>
          </li>
          <li>
            Please fill out the available form with accurate information and
            click&nbsp;<strong>Submit</strong> at the bottom of the page
          </li>
          <li>
            Once you have successfully submitted the form, you will receive an
            email containing login credentials for accessing your Author
            Dashboard.&nbsp;
            <em>
              It is important to note that this account is separate from
              Police&nbsp;Technical&nbsp;user accounts
            </em>
          </li>
          <li>
            Once you have signed into your Police Technical author account, you
            will see the tab&nbsp;<strong>Books</strong>
          </li>
          <li>
            Under this tab you will see the option to&nbsp;
            <strong>Add a Book</strong>
          </li>
          <li>
            After completing the required form on this page with information
            regarding the current information and status of your book/outline,
            you will click&nbsp;<strong>Submit Book&nbsp;</strong> at the bottom
            of the page
          </li>
          <li>
            Your book will now appear under the&nbsp;
            <strong>Books&nbsp;</strong>tab, and will allow you to view the
            required documents to upload based on your books publication status
          </li>
          <li>
            After submission of these files, our editorial team will review your
            uploaded material and continue the process from there
          </li>
        </ul>
      ),
    },
    {
      id: 6,
      question: "Purchasing Certification Track Credits",
      answer: (
        <ul>
          <li>
            <a href="/course/tracks">
              Visit the Purchase Certification Tracks page
            </a>
          </li>
          <li>
            You must be signed in to Police Technical in order to access this
            page
          </li>
          <li>
            Click the <strong>purchase</strong> button next to
            the&nbsp;certification track you are interested in
          </li>
          <li>
            Select an elective if you have not yet completed one for that track
          </li>
          <li>
            Click <strong>checkout</strong> to proceed to&nbsp;the payment
            gateway
          </li>
          <li>
            <em>
              This process can also be completed under the
              <strong> Certification Track</strong> tab on your profile page
            </em>
          </li>
        </ul>
      ),
    },
    {
      id: 7,
      question: "Using Your Course Credits",
      answer: (
        <ul>
          <li>
            You must be signed into your Police Technical account in order to
            use your Course Credits
          </li>
          <li>
            Once you are signed in, navigate to&nbsp;the class you would like to
            attend from our&nbsp;
            <a href="/classes/">Training Schedule</a>
          </li>
          <li>
            If you have an available course credit for the course associated
            with this class, an extra tab will appear next to the Class Flyer
            tab titled&nbsp;<strong>Course Credit</strong>
          </li>
          <li>
            Under this tab you will be able to register for the class by simply
            clicking the&nbsp;
            <strong>Register using course credits&nbsp;</strong>button
          </li>
        </ul>
      ),
    },
  ];

  return (
    <div>
      <BreadCrumbs list={["Home", "FAQ"]} title="FAQ" />
      <div className="container">
        <div id="faq">
          {faqs.map((faq, i) => (
            <div className="card my-3" key={i}>
              <a
                className="card-header card-link bg-light text-primary"
                data-toggle="collapse"
                href={`#f-${faq.id}`}
              >
                <h4>{faq.question}</h4>
              </a>
              <div
                id={`f-${faq.id}`}
                className={`card-body bg-light collapse ${
                  i === 0 ? "show" : ""
                }`}
                data-parent="#faq"
              >
                <p>{faq.answer}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <br />
      <div className="row"></div>
    </div>
  );
};

export default Faq;
