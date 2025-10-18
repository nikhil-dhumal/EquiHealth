import client from "./clients/client.js";

const endpoints = {
  getDistricts: "districts",
};

const districtsApi = {
  getDistricts: async () => {
    try {
      const res = await client.get(endpoints.getDistricts);
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default districtsApi;
