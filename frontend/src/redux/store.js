import { configureStore } from "@reduxjs/toolkit";

import activePageSlice from "./features/activePageSlice";
import healthInfraSlice from "./features/healthInfraSlice";

const store = configureStore({
  reducer: {
    activePage: activePageSlice,
    healthInfra: healthInfraSlice,
  },
});

export default store;
