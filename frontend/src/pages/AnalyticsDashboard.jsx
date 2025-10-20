import React, { useState } from "react";

import Map from "../components/common/Map.jsx";
import SelectFilters from "../components/common/SelectFilters.jsx";

const AnalyticsDashboard = () => {
  const [selected, setSelected] = useState({
    state: null,
    district: null,
    hospital: null,
  });

  return (
    <div id="analytics-dashboard">
      <SelectFilters selected={selected} setSelected={setSelected} />
      <Map selected={selected} />
    </div>
  );
};

export default AnalyticsDashboard;
