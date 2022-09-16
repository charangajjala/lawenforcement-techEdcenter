import React from "react";

const Error = ({ err }) => {
  return (
    <div>
      <h1>{err.message}</h1>
    </div>
  );
};

export default Error;
