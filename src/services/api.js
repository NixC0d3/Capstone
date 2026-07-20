// Purpose: Central place for API calls to the Flask backend. Views call these functions instead of writing fetch code repeatedly.
// VITE_API_BASE_URL can point Vue to Flask, for example http://localhost:5001/api.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

// Small wrapper around fetch so all API requests handle JSON and errors consistently.
async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

    // Some responses may not contain JSON, so return an empty object instead of crashing.
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "API request failed");
  }

  return data;
}

// These methods are imported by views/components when they need backend data.
export const api = {
  getOrganisations() {
    return request("/organisations");
  },

  getOrganisation(id) {
    return request(`/organisations/${id}`);
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
