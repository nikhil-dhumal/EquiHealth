import { configureStore } from "@reduxjs/toolkit";

import activePageSlice from "./features/activePageSlice";
import statesSlice from "./features/statesSlice";
import districtsSlice from "./features/districtsSlice";

const store = configureStore({
  reducer: {
    activePage: activePageSlice,
    states: statesSlice,
    districts: districtsSlice,
  },
});

export default store;
