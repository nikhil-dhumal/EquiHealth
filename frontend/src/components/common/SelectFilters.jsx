import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Select from "react-select";

import districtApi from "../../api/modules/districtsApi.js";
import hospitalsApi from "../../api/modules/hospitalsApi.js";

import { setDistricts } from "../../redux/features/districtsSlice.js";
import { setHospitals } from "../../redux/features/hospitalsSlice.js";

const selectStyles = {
  control: (base, state) => ({
    ...base,
    border: "none",
    borderBottom: state.isDisabled ? "none" : "2px solid #1565C0",
    borderRadius: 0,
    boxShadow: "none",
    zIndex: 10000,
    backgroundColor: state.isDisabled ? "#eeeeee" : "#ffffff",
    "&:hover": {
      borderBottom: state.isDisabled ? "none" : "2px solid #1565C0",
    },
  }),
  menu: (base) => ({
    ...base,
    zIndex: 9999,
  }),
  dropdownIndicator: (base, state) => ({
    ...base,
    color: state.isDisabled ? "#bdbdbd" : "#1565C0",
    "&:hover": {
      color: state.isDisabled ? "#bdbdbd" : "#1565C0",
    },
  }),
  clearIndicator: (base, state) => ({
    ...base,
    color: state.isDisabled ? "#bdbdbd" : "#E53935",
    "&:hover": {
      color: state.isDisabled ? "#bdbdbd" : "#E53935",
    },
  }),
};

const SelectFilters = ({ selected, setSelected }) => {
  const dispatch = useDispatch();

  const { states } = useSelector((state) => state.states);
  const { districts } = useSelector((state) => state.districts);
  const { hospitals } = useSelector((state) => state.hospitals);

  const handleStateChange = async (option) => {
    const stateId = option?.value;

    const { res: districtRes, err: districtErr } =
      await districtApi.getDistricts({ stateId });
    if (districtRes) dispatch(setDistricts(districtRes));
    if (districtErr) console.error(districtErr);

    const { res: hospitalRes, err: hospitalErr } =
      await hospitalsApi.getHospitals({ stateId });
    if (hospitalRes) dispatch(setHospitals(hospitalRes));
    if (hospitalErr) console.error(hospitalErr);

    setSelected({
      state: option,
      district: null,
      hospital: null,
    });
  };

  const handleDistrictChange = async (option) => {
    const districtId = option?.value;
    const stateId = selected.state.value;

    const { res, err } = await hospitalsApi.getHospitals({
      stateId,
      districtId,
    });
    if (res) dispatch(setHospitals(res));
    if (err) console.error(err);

    setSelected((prev) => ({
      ...prev,
      district: option,
      hospital: null,
    }));
  };

  const handleHospitalChange = (option) => {
    setSelected((prev) => ({
      ...prev,
      hospital: option,
    }));
  };

  useEffect(() => {
    const fetchHospitals = async () => {
      const { res, err } = await hospitalsApi.getHospitals();
      if (res) dispatch(setHospitals(res));
      else dispatch(setHospitals([]));
    };

    fetchHospitals();
  }, [dispatch]);

  return (
    <div className="select-filters">
      <Select
        className="filter"
        styles={selectStyles}
        value={selected.state}
        options={states.map((s) => ({
          value: s.state_id,
          label: s.state_name,
          latitude: s.latitude,
          longitude: s.longitude,
        }))}
        onChange={handleStateChange}
        placeholder="Select State"
        isClearable
      />
      <Select
        className="filter"
        styles={selectStyles}
        value={selected.district}
        options={districts.map((d) => ({
          value: d.district_id,
          label: d.district_name,
          latitude: d.latitude,
          longitude: d.longitude,
        }))}
        onChange={handleDistrictChange}
        placeholder="Select District"
        isDisabled={!selected.state?.value}
        isClearable
      />
      <Select
        className="filter"
        styles={selectStyles}
        value={selected.hospital}
        options={hospitals.map((h) => ({
          value: h.hospital_id,
          label: h.hospital_name,
          latitude: h.latitude,
          longitude: h.longitude,
        }))}
        onChange={handleHospitalChange}
        placeholder="Select Hospital"
        isDisabled={!selected.district?.value}
        isClearable
      />
    </div>
  );
};

export default SelectFilters;
