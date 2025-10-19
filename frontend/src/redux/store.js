import { configureStore } from "@reduxjs/toolkit";

import activePageSlice from "./features/activePageSlice";
import statesSlice from "./features/statesSlice";

const store = configureStore({
  reducer: {
    activePage: activePageSlice,
    states: statesSlice,
  },
});

export default store;
