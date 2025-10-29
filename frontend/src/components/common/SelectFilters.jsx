import React from "react";
import { useSelector } from "react-redux";
import Select from "react-select";

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
  const { states, districts, hospitals } = useSelector(
    (state) => state.healthInfra
  );

  const stateOptions = states.allIds.map((id) => {
    const s = states.byId[id];
    return {
      value: s.state_id,
      label: s.state_name,
    };
  });

  const districtOptions = selected.state
    ? states.byId[selected.state.value].districts.map((distId) => {
        const d = districts.byId[distId];
        return {
          value: d.district_id,
          label: d.district_name,
        };
      })
    : [];

  const hospitalOptions = selected.district
    ? districts.byId[selected.district.value].hospitals.map((hId) => {
        const h = hospitals.byId[hId];
        return {
          value: h.hospital_id,
          label: h.hospital_name,
        };
      })
    : [];

  const handleStateChange = (option) => {
    setSelected({
      state: option,
      district: null,
      hospital: null,
    });
  };

  const handleDistrictChange = (option) => {
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

  return (
    <div className="select-filters">
      <Select
        className="filter"
        styles={selectStyles}
        value={selected.state}
        options={stateOptions}
        onChange={handleStateChange}
        placeholder="Select State"
        isClearable
      />
      <Select
        className="filter"
        styles={selectStyles}
        value={selected.district}
        options={districtOptions}
        onChange={handleDistrictChange}
        placeholder="Select District"
        isDisabled={!selected.state}
        isClearable
      />
      <Select
        className="filter"
        styles={selectStyles}
        value={selected.hospital}
        options={hospitalOptions}
        onChange={handleHospitalChange}
        placeholder="Select Hospital"
        isDisabled={!selected.district}
        isClearable
      />
    </div>
  );
};

export default SelectFilters;
