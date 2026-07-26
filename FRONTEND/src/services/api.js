const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5001/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "API request failed");
  }

  return data;
}

export const api = {
  getOrganisations(params = {}) {
  const query = new URLSearchParams(params).toString();
  return request(`/organisations${query ? `?${query}` : ""}`);
  },

  getOrganisation(id) {
    return request(`/organisations/${id}`);
  },

  getCategories() {
    return request("/organisations/categories");
  },
  
  getLocations(){
    return request("/organisations/locations");
  },

  getMonthlyReport(id){
    return request(`/reports/monthly-report/${id}`);
},
  registerUser(payload){
    return request("/auth/register", {
      method:"POST",
      body:JSON.stringify(payload)
    });
  },

  getRecommendations(userId, type = "business", limit = 6) {
  return request(`/recommendations/user/${userId}?type=${type}&limit=${limit}`);
  },
  
  createReview(reviewData) {
    return request("/reviews", {
      method: "POST",
      body: JSON.stringify(reviewData)
    });
  },

  getOrganisationReviews(organisationId) {
    return request(`/reviews/organisation/${organisationId}`);
  },

  getVolunteerNeeds() {
    return request("/volunteers/needs");
  },
  
  logEngagement(data) {
    return request("/engagement/log", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },
  
  saveOrganisation(data) {
    return request("/saves", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },

  unsaveOrganisation(data) {
    return request("/saves", {
      method: "DELETE",
      body: JSON.stringify(data)
    });
  },

  calculateTrendScore(payload) {
    return request("/reports/trend-score", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  },

  getEngagementWeights() {
    return request("/admin/engagement-weights");
  },
  
  getConversation(userId, organisationId) {
    return request(`/messages/conversation?user_id=${userId}&organisation_id=${organisationId}`);
  },

  
  sendMessage(data) {
    return request("/messages/send", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },

  updateEngagementWeights(payload) {
    return request("/admin/engagement-weights", {
      method: "PUT",
      body: JSON.stringify(payload)
    });
  }
};
