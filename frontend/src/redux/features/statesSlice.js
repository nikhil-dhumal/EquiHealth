import { createSlice } from "@reduxjs/toolkit";
import { capitalizeWords } from "../../utils/formatters";

export const stateSlice = createSlice({
  name: "States",
  initialState: {
    states: [],
  },
  reducers: {
    setStates: (state, action) => {
      const { count, data } = action.payload
      state.states = data.map((s) => ({
        ...s,
        state_name: capitalizeWords(s.state_name),
      }));
    },
  },
});

export const { setStates } = stateSlice.actions;

export default stateSlice.reducer;
