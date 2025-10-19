import { createSlice } from "@reduxjs/toolkit";

export const districtsSlice = createSlice({
  name: "Districts",
  initialState: {
    districts: [],
  },
  reducers: {
    setDistricts: (state, action) => {
      const { count, data } = action.payload
      state.districts = [...data];
    },
  },
});

export const { setDistricts } = districtsSlice.actions;

export default districtsSlice.reducer;
