import client from "../clients/client.js";

const endpoints = {
  getHospitals: "hospitals",
  getHospitalsCompact: "hospitals/compact",
  getHospitalsGrouped: "hospitals/grouped",
};

const hospitalsApi = {
  getHospitals: async ({ stateId, districtId, hospitalId } = {}) => {
    try {
      const params = {};
      if (stateId) params.state_id = stateId;
      if (districtId) params.district_id = districtId;
      if (hospitalId) params.hospital_id = hospitalId;
      const res = await client.get(endpoints.getHospitals, { params });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getHospitalsCompact: async ({ stateId, districtId, hospitalId } = {}) => {
    try {
      const params = {};
      if (stateId) params.state_id = stateId;
      if (districtId) params.district_id = districtId;
      if (hospitalId) params.hospital_id = hospitalId;
      const res = await client.get(endpoints.getHospitalsCompact, { params });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getHospitalsGrouped: async ({ stateId, districtId } = {}) => {
    try {
      const params = {};
      if (stateId) params.state_id = stateId;
      if (districtId) params.district_id = districtId;
      const res = await client.get(endpoints.getHospitalsGrouped, { params });
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default hospitalsApi;
