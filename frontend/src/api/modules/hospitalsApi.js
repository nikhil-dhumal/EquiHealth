import client from "./clients/client.js";

const endpoints = {
  getHospitals: "hospitals",
  getHospitalsCompact: "hospitals/compact",
  getHospitalsGrouped: "hospitals/grouped",
};

const hospitalsApi = {
  getHospitals: async ({ stateId, districtId, hospitalId }) => {
    try {
      const res = await client.get(endpoints.getHospitals, {
        params: {
          state_id: stateId,
          district_id: districtId,
          hospital_id: hospitalId,
        },
      });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getHospitalsCompact: async ({ stateId, districtId, hospitalId }) => {
    try {
      const res = await client.get(endpoints.getHospitalsCompact, {
        params: {
          state_id: stateId,
          district_id: districtId,
          hospital_id: hospitalId,
        },
      });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getHospitalsGrouped: async ({ stateId, districtId }) => {
    try {
      const res = await client.get(endpoints.getHospitalsGrouped, {
        params: {
          state_id: stateId,
          district_id: districtId,
        },
      });
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default hospitalsApi;
