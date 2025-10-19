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
    (async () => {
      const { res, err } = await statesApi.getStates();
      if (res) dispatch(setStates(res));
      if (err) console.log(err);
    })();
    (async () => {
      const { res, err } = await hospitalsApi.getHospitals()
      if (res) dispatch(setHospitals(re))
      if (err) dispatch(setHospitals([]))
    })
  }, []);

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
