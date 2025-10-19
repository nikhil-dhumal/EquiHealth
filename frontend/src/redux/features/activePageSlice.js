import { createSlice } from "@reduxjs/toolkit";

export const activePageSlice = createSlice({
  name: "ActivePage",
  initialState: {
    activePage: 0,
  },
  reducers: {
    setActivePage: (state, action) => {
      state.activePage = action.payload;
    },
  },
});

export const { setActivePage } = activePageSlice.actions;

export default activePageSlice.reducer;
