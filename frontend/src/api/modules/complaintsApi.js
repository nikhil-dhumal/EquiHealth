import client from "../clients/client.js";

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
  } = {}) => {
    try {
      const params = {};
      if (stateId) params.state_id = stateId;
      if (districtId) params.district_id = districtId;
      if (hospitalId) params.hospital_id = hospitalId;
      if (search) params.search = search;
      if (page) params.page = page;
      if (pageSize) params.page_size = pageSize;
      if (orderBy) params.order_by = orderBy;
      if (orderDir) params.order_dir = orderDir;
      const res = await client.get(endpoints.getComplaints, { params });
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
