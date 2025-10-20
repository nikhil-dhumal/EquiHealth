import client from "../clients/client.js";

const endpoints = {
  getName: "users",
};

const userApi = {
  getName: async ({ phoneNumber }) => {
    try {
      const res = await client.get(endpoints.getName, {
        params: {
          phone_number: phoneNumber,
        },
      });
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default userApi;
