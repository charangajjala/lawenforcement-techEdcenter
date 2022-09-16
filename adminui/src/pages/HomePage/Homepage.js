import React from "react";
import BreadCrumbs from "../../util/components/BreadCrumbs";

const HomePage = () => {

  const list = ["Home"];
  return (
    <>
      <BreadCrumbs list={list} />
      <h1>Homepage</h1>
    </>
  );
};
export default HomePage;
