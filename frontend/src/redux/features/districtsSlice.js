import { createSlice } from "@reduxjs/toolkit";
import { capitalizeWords } from "../../utils/formatters";

export const districtsSlice = createSlice({
  name: "Districts",
  initialState: {
    districts: [],
  },
  reducers: {
    setDistricts: (state, action) => {
      const { count, data } = action.payload
      state.districts = data.map((d) => ({
        ...d,
        district_name: capitalizeWords(d.district_name),
      }));
    },
  },
});

export const { setDistricts } = districtsSlice.actions;

export default districtsSlice.reducer;
