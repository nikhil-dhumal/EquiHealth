import { createSlice } from "@reduxjs/toolkit";

export const stateSlice = createSlice({
  name: "States",
  initialState: {
    states: [],
  },
  reducers: {
    setStates: (state, action) => {
      const { count, data } = action.payload
      state.states = [...data];
    },
  },
});

export const { setStates } = stateSlice.actions;

export default stateSlice.reducer;
