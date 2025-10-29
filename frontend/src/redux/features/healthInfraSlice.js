import { createSlice } from "@reduxjs/toolkit";

import { capitalizeWords } from "../../utils/formatters";

export const healthInfraSlice = createSlice({
  name: "healthInfra",
  initialState: {
    states: { byId: {}, allIds: [] },
    districts: { byId: {}, allIds: [] },
    hospitals: { byId: {}, allIds: [] },
  },
  reducers: {
    setHealthInfra: (state, action) => {
      const { data } = action.payload;

      state.states = { byId: {}, allIds: [] };
      state.districts = { byId: {}, allIds: [] };
      state.hospitals = { byId: {}, allIds: [] };

      data.forEach((stateObj) => {
        const stateId = stateObj.state_id;

        const formattedState = {
          ...stateObj,
          state_name: capitalizeWords(stateObj.state_name),
          districts: stateObj.districts.map((d) => d.district_id),
        };

        state.states.byId[stateId] = formattedState;
        state.states.allIds.push(stateId);

        stateObj.districts.forEach((district) => {
          const districtId = district.district_id;

          // ✅ Capitalize district name
          const formattedDistrict = {
            ...district,
            district_name: capitalizeWords(district.district_name),
            state_id: stateId,
            hospitals: district.hospitals.map((h) => h.hospital_id),
          };

          state.districts.byId[districtId] = formattedDistrict;
          state.districts.allIds.push(districtId);

          district.hospitals.forEach((hospital) => {
            const hospitalId = hospital.hospital_id;

            // ✅ Capitalize hospital name + address
            const formattedHospital = {
              ...hospital,
              hospital_name: capitalizeWords(hospital.hospital_name),
              address: hospital.address
                ? capitalizeWords(hospital.address)
                : "",
              state_id: stateId,
              district_id: districtId,
            };

            state.hospitals.byId[hospitalId] = formattedHospital;
            state.hospitals.allIds.push(hospitalId);
          });
        });
      });

      state.loaded = true;
    },
  },
});

export const { setHealthInfra } = healthInfraSlice.actions;

export default healthInfraSlice.reducer;
