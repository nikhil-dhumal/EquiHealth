import { configureStore } from "@reduxjs/toolkit";

import activePageSlice from "./features/activePageSlice";
import statesSlice from "./features/statesSlice";
import districtsSlice from "./features/districtsSlice";
import hospitalsSlice from "./features/hospitalsSlice";

const store = configureStore({
  reducer: {
    activePage: activePageSlice,
    states: statesSlice,
    districts: districtsSlice,
    hospitals: hospitalsSlice,
  },
});

export default store;
