import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { Outlet } from "react-router-dom";

import statesApi from "../../api/modules/statesApi.js";

import NavBar from "../common/Navbar";
import Footer from "../common/Footer";

import { setStates } from "../../redux/features/statesSlice.js";

const MainLayout = () => {
  const dispatch = useDispatch();

  useEffect(() => {
  const fetchStates = async () => {
    const { res, err } = await statesApi.getStates();
    if (res) dispatch(setStates(res));
    else if (err) console.log(err);
  };

  fetchStates();
}, [dispatch]);

  return (
    <>
      <NavBar />
      <main>
        <Outlet />
      </main>
      <Footer />
    </>
  );
};

export default MainLayout;
