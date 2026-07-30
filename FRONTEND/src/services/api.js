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
  
  // Organisations
  getOrganisations(params = {}) {
  const query = new URLSearchParams(params).toString();
  return request(`/organisations${query ? `?${query}` : ""}`);
  },
  
  getOrganisation(id) {
    return request(`/organisations/${id}`);
  },

  createOrganisation(data) {
    return request("/organisations", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },

  updateOrganisation(id, data) {
    return request(`/organisations/${id}`, {
      method: "PUT",
      body: JSON.stringify(data)
    });
  },

  getOwnerOrganisation(userId) {
    return request(`/organisations/owner/${userId}`);
  },
  
  getCategories() {
    return request("/organisations/categories");
  },
  getLocations(){
    return request("/organisations/locations");
  },
  
  // Registration
  registerUser(payload){
    return request("/auth/register", {
      method:"POST",
      body:JSON.stringify(payload)
    });
  },
  login(payload) {
    return request("/auth/login", {
        method: "POST",
        body: JSON.stringify(payload)
    });
  },
  getProfile(userId) {
    return request(`/auth/profile/${userId}`);
  },

  // Recommendations
  getRecommendations(userId, type = "business", limit = 6) {
  return request(`/recommendations/user/${userId}?type=${type}&limit=${limit}`);
  },
  
  // Reviews
  createReview(reviewData) {
    return request("/reviews", {
      method: "POST",
      body: JSON.stringify(reviewData)
    });
  },
  flagReview(reviewId, payload) {
    return request(`/reviews/${reviewId}/flag`, {method: "POST", body: JSON.stringify(payload)});
  },
  getOrganisationReviews(organisationId) {
    return request(`/reviews/organisation/${organisationId}`);
  },

  // Volunteers
  createVolunteerNeed(data) {
    return request("/volunteer-allocation/needs", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },
  
  getVolunteerNeeds(charityUserId) {
    return request(`/volunteer-allocation/needs?charity_user_id=${charityUserId}`);
  },

  getVolunteerMatches(volunteerNeedId, charityUserId) {
    return request(`/volunteer-allocation/need/${volunteerNeedId}/matches?charity_user_id=${charityUserId}`);
  },

  allocateVolunteer(volunteerNeedId, data) {
    return request(`/volunteer-allocation/need/${volunteerNeedId}/allocate`, {
      method: "POST",
      body: JSON.stringify(data)
    });
  },
  
  declineVolunteer(volunteerNeedId, data) {
    return request(`/volunteer-allocation/need/${volunteerNeedId}/decline`, {
      method: "POST",
      body: JSON.stringify(data)
    });
  },
  
  getVolunteerOpportunities(userId = null) {
    const query = userId ? `?user_id=${userId}` : "";
    return request(`/volunteer-allocation/opportunities${query}`);
  },

  signupVolunteer(data) {
    return request("/volunteer-allocation/signup", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },

  getMyVolunteerApplications(userId) {
    return request(`/volunteer-allocation/my-applications?user_id=${userId}`);
  },
  
  // Saved Organisations
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
  getSavedOrganisations(userId) {
    return request(`/saves?user_id=${userId}`);
  },

  // Reports
  getMonthlyReport(id) {
    return request(`/reports/monthly-report/${id}`);
  },

  getOrganisationDashboardReport(organisationId) {
    return request(`/organisations/${organisationId}/dashboard-report`);
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
  
  logEngagement(data) {
    return request("/engagement/log", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },
  
  // Messages
  getInbox(userId) {
    return request(`/messages/inbox?user_id=${userId}`);
  },

  getConversation(userId, organisationId) {
    return request(`/messages/conversation?user_id=${userId}&organisation_id=${organisationId}`);
  },

  getConversationById(conversationId, userId) {
    return request(`/messages/conversation/${conversationId}?user_id=${userId}`);
  },

  sendMessage(data) {
    return request("/messages/send", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }, 
   getBusinessDashboardReport(userId) {
    return request(`/reports/business-dashboard/${userId}`);
  },  
  getConversationById(conversationId, userId) {
    return request(`/messages/conversation/${conversationId}?user_id=${userId}`);
  },

  // Admin
  getUsers(status = "all"){
    return request(`/admin/users?status=${status}`);
  },
  getEngagementWeights(){
    return request("/admin/engagement-weights");
  },
  updateEngagementWeights(payload) {
    return request("/admin/engagement-weights", {
      method: "PUT",
      body: JSON.stringify(payload)
    });
  },
  getUserDetails(id){
    return request(`/admin/users/${id}`);
  },
  reviewUser(id,data){
      return request(`/admin/users/${id}/review`,{
          method:"POST",
          body:JSON.stringify(data)
      });
  },
  // Admin organisations
  getAdminOrganisations(){
      return request("/admin/organisations");
  },
  getAdminOrganisation(id) {
    return request(`/admin/organisations/${id}`);
  },
  
  //Uer MAnagement
  getProfile(userId){
    return request(`/users/${userId}/profile`);
  },
  updateProfile(userId,data){
      return request(`/users/${userId}/profile`,{
          method:"PUT",
          body:JSON.stringify(data)
      });
  },

  getSkills(){
      return request("/users/skills");
  },

  updateSkills(userId,skills){
      return request(`/users/${userId}/skills`,{
          method:"PUT",
          body:JSON.stringify({
              skills
          })
      });
  },

  getInterests(){
      return request("/users/interests");
  },

  updateInterests(userId,categories){
      return request(`/users/${userId}/interests`,{
          method:"PUT",
          body:JSON.stringify({
              categories
          })
      });
  }
};
