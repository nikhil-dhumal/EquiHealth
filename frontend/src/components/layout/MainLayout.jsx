import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { Outlet } from "react-router-dom";

import statesApi from "../../api/modules/statesApi.js";
import hospitalsApi from "../../api/modules/hospitalsApi.js";

import NavBar from "../common/Navbar";
import Footer from "../common/Footer";

import { setStates } from "../../redux/features/statesSlice.js";
import { setHospitals } from "../../redux/features/hospitalsSlice.js";

const MainLayout = () => {
  const dispatch = useDispatch();

  useEffect(() => {
  const fetchStates = async () => {
    const { res, err } = await statesApi.getStates();
    if (res) dispatch(setStates(res));
    else if (err) console.log(err);
  };

  const fetchHospitals = async () => {
    const { res, err } = await hospitalsApi.getHospitals();
    if (res) dispatch(setHospitals(res));
    else dispatch(setHospitals([]));
  };

  fetchStates();
  fetchHospitals();
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
