import { configureStore } from "@reduxjs/toolkit";

import activePageSlice from "./features/activePageSlice";

const store = configureStore({
  reducer: {
    activePage: activePageSlice,
  },
});

export default store;
