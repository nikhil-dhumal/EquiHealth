import { createSlice } from "@reduxjs/toolkit";

export const stateSlice = createSlice({
  name: "States",
  initialState: {
    states: [],
  },
  reducers: {
    setStates: (state, action) => {
      state.activePage = action.payload;
    },
  },
});

export const { setStates } = stateSlice.actions;

export default stateSlice.reducer;
