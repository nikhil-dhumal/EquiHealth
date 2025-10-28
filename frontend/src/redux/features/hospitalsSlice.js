import { createSlice } from "@reduxjs/toolkit";
import { capitalizeWords } from "../../utils/formatters";

export const hospitalsSlice = createSlice({
  name: "Hospitals",
  initialState: {
    hospitals: [],
  },
  reducers: {
    setHospitals: (state, action) => {
      const { count, data } = action.payload
      state.hospitals = data.map((h) => ({
        ...h,
        hospital_name: capitalizeWords(h.hospital_name),
      }));
    },
  },
});

export const { setHospitals } = hospitalsSlice.actions;

export default hospitalsSlice.reducer;
