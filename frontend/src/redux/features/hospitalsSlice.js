import { createSlice } from "@reduxjs/toolkit";

export const hospitalsSlice = createSlice({
  name: "Hospitals",
  initialState: {
    hospitals: [],
  },
  reducers: {
    setHospitals: (state, action) => {
      const { count, data } = action.payload
      state.hospitals = [...data];
    },
  },
});

export const { setHospitals } = hospitalsSlice.actions;

export default hospitalsSlice.reducer;
