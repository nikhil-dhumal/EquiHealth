import client from "./clients/client.js";

const endpoints = {
  postComplaint: "complaints",
  getComplaints: "complaints",
  getComplaintById: (complaintId) => `complaints/${complaintId}`,
};

const complaintsApi = {
  postComplaint: async ({
    phoneNumber,
    name,
    stateId,
    districtId,
    hospitalId,
    title,
    details,
  }) => {
    try {
      const res = await client.post(endpoints.postComplaint, {
        phoneNumber,
        name,
        stateId,
        districtId,
        hospitalId,
        title,
        details,
      });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getComplaints: async ({
    stateId,
    districtId,
    hospitalId,
    search,
    page,
    pageSize,
    orderBy,
    orderDir,
  }) => {
    try {
      const res = await client.get(endpoints.getComplaints, {
        params: {
          state_id: stateId,
          district_id: districtId,
          hospital_id: hospitalId,
          search: search,
          page: page,
          page_size: pageSize,
          order_by: orderBy,
          order_dir: orderDir,
        },
      });
      return { res };
    } catch (err) {
      return { err };
    }
  },
  getComplaintById: async ({ complaintId }) => {
    try {
      const res = await client.get(endpoints.getComplaintById(complaintId));
      return { res };
    } catch (err) {
      return { err };
    }
  },
};

export default complaintsApi;
