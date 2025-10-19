import client from "../clients/client.js";

const endpoints = {
  getStates: "states",
};

const statesApi = {
  getStates: async () => {
    try {
      const res = await client.get(endpoints.getStates);
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default statesApi;
