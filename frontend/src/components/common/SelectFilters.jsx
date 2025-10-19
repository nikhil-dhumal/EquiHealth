import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import districtApi from "../../api/modules/districtsApi.js";
import hospitalsApi from "../../api/modules/hospitalsApi.js";

import { setDistricts } from "../../redux/features/districtsSlice.js";
import { setHospitals } from "../../redux/features/hospitalsSlice.js";

const SelectFilters = ({ selected, setSelected }) => {
  const dispatch = useDispatch();

  const { states } = useSelector((state) => state.states);
  const { districts } = useSelector((state) => state.districts);
  const { hospitals } = useSelector((state) => state.hospitals);

  const handleStateChange = async (e) => {
    (async () => {
      const { res, err } = await districtApi.getDistricts({
        stateId: e.target.value,
      });
      if (res) dispatch(setDistricts(res));
      if (err) console.log(err);
    })();
    (async () => {
      const { res, err } = await hospitalsApi.getHospitals({
        stateId: e.target.value,
      });
      if (res) dispatch(setHospitals(res));
      if (err) console.log(err);
    })();
    setSelected({ state: e.target.value, district: "", hospital: "" });
  };

  const handleDistrictChange = async (e) => {
    (async () => {
      const { res, err } = await hospitalsApi.getHospitals({
        stateId: selected.state,
        districtId: e.target.value,
      });
      if (res) dispatch(setHospitals(res));
      if (err) console.log(err);
    })();
    setSelected((prev) => ({
      state: prev.state,
      district: e.target.value,
      hospital: "",
    }));
  };

  const handleHospitalChange = async (e) => {
    (async () => {
      const { res, err } = await hospitalsApi.getHospitals({
        stateId: selected.state,
        districtId: selected.district,
        hospitalId: e.target.value,
      });
      if (res) dispatch(setHospitals(res));
      if (err) console.log(err);
    })();
    setSelected((prev) => ({ ...prev, hospital: e.target.value }));
  };

  return (
    <div className="select-filters">
      <select value={selected.state} onChange={handleStateChange}>
        <option value="">Select State</option>
        {states.map((state) => (
          <option key={state.state_id} value={state.state_id}>
            {state.state_name}
          </option>
        ))}
      </select>

      <select
        value={selected.district}
        onChange={handleDistrictChange}
        disabled={!selected.state}
      >
        <option value="">Select District</option>
        {districts.map((district) => (
          <option key={district.district_id} value={district.district_id}>
            {district.district_name}
          </option>
        ))}
      </select>

      <select
        value={selected.hospital}
        onChange={handleHospitalChange}
        disabled={!selected.district}
      >
        <option value="">Select Hospital</option>
        {hospitals.map((hospital) => (
          <option key={hospital.hospital_id} value={hospital.hospital_id}>
            {hospital.hospital_name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SelectFilters;
