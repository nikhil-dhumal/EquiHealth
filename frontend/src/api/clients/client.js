import axios from "axios";

const baseURL = import.meta.env.VITE_BACKEND_URL;

const client = axios.create({
  baseURL,
  paramsSerializable: {
    serialize: (params) => {
      const searchParams = new URLSearchParams();
      Object.keys(params).forEach((key) => {
        searchParams.append(key, params[key]);
      });
      return searchParams.toString();
    },
  },
});

client.interceptors.request.use(async (config) => {
  return {
    ...config,
    headers: {
      "Content-Type": "application/json",
    },
  };
});

client.interceptors.response.use(
  async (response) => {
    if (response?.data) return response.data;
    return response;
  },
  (error) => {
    const message = error?.response?.data?.message;
    if (message) throw message || "Something went wrong. Please try again.";
    throw error;
  }
);

export default client;
