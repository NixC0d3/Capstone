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
  getOrganisations() {
    return request("/organisations");
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

  registerUser(payload){
    return request("/auth/register", {
      method:"POST",
      body:JSON.stringify(payload)
    });
  },

  getRecommendations(userId) {
    return request(`/recommendations/${userId}`);
  },

  getVolunteerNeeds() {
    return request("/volunteers/needs");
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

  updateEngagementWeights(payload) {
    return request("/admin/engagement-weights", {
      method: "PUT",
      body: JSON.stringify(payload)
    });
  }
};
