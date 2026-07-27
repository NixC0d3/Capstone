<template>
  <div class="dashboard">

    <p class="subtitle">
      Find small businesses worth supporting
    </p>

    <h1>Explore your Community</h1>

    <SearchBar
      v-model:searchTerm="searchTerm"
      v-model:category="selectedCategory"
      v-model:location="selectedLocation"
      :categories="categories"
      :locations="locations"
      @search="searchOrganizations"
    />

    <!-- SEARCH RESULTS SECTION -->
    <div v-if="hasSearched">
      <button class="back-button" @click="goBack">
        ← Clear Search
      </button>

      <h2>Search Results</h2>

      <div v-if="organisations.length" class="card-grid">
        <OrganisationCard
          v-for="org in organisations"
          :key="org.organisation_id"
          :organisation="org"
        />
      </div>

      <p v-else>
        No organisations match your search.
      </p>
    </div>

    <!-- RECOMMENDATIONS SECTION -->
    <div v-else>
      <h2>Recommended for you</h2>

      <div v-if="recommendedOrganisations.length" class="card-grid">
        <OrganisationCard
          v-for="org in recommendedOrganisations"
          :key="org.organisation_id"
          :organisation="org"
        />
      </div>

      <p v-else>
        No recommendations available yet.
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import SearchBar from "@/components/SearchBar.vue";
import OrganisationCard from "@/components/OrganisationCard.vue";

import { api } from "@/services/api";


const organisations = ref([]);
const recommendedOrganisations = ref([]);

const categories = ref([]);
const locations = ref([]);

const searchTerm = ref("");
const selectedCategory = ref("");
const selectedLocation = ref("");

const hasSearched = ref(false);

/*
  ADD SAVED STATUS TO ORGANISATIONS
*/
async function addSavedStatus(orgs) {
  const user = JSON.parse(localStorage.getItem("user"));
  // If no user is logged in, everything is unsaved
  if (!user || !user.user_id) {

    return orgs.map(org => ({
      ...org,
      is_saved: false
    }));
  }  
  try {

    const savedOrganisations = await api.getSavedOrganisations(user.user_id);

    return orgs.map(org => ({
      ...org,
      is_saved: savedOrganisations.some(
        saved => saved.organisation_id === org.organisation_id
    )}));
  } catch (error) {
    console.error("Error loading saved organisations:", error);
    return orgs.map(org => ({
      ...org,
      is_saved: false
    }));
  }
}

/*
  LOAD RECOMMENDATIONS
*/
async function loadRecommendations() {
  try {
    const user = JSON.parse(localStorage.getItem("user"));

    console.log("Logged in user:", user);

    if (!user || !user.user_id) {
      console.log("No logged-in user found in localStorage.");
      return;
    }

    const data = await api.getRecommendations(user.user_id, "business", 6);

    console.log("Recommendations from backend:", data);

    recommendedOrganisations.value = await addSavedStatus(data);
  } catch (error) {
    console.error("Error loading recommendations:", error);
  }
}


/*
  LOAD CATEGORIES AND LOCATIONS
*/
async function loadFilters() {
  try {
    categories.value = await api.getCategories();
    locations.value = await api.getLocations();

    console.log("Categories:", categories.value);
    console.log("Locations:", locations.value);
  } catch (error) {
    console.error("Error loading filters:", error);
  }
}


/*
  PAGE LOAD
*/
onMounted(async () => {
  await loadFilters();
  await loadRecommendations();
});


/*
  SEARCH ORGANISATIONS FROM DATABASE
*/
async function searchOrganizations() {
  try {
    hasSearched.value = true;

    organisations.value = await api.getOrganisations({
      search: searchTerm.value,
      category_id: selectedCategory.value,
      parish: selectedLocation.value,
      type: "business"
    });

    console.log("Search results:", organisations.value);
  } catch (error) {
    console.error("Error searching organisations:", error);
  }
}


/*
  CLEAR SEARCH AND RETURN TO RECOMMENDATIONS
*/
async function goBack() {
  hasSearched.value = false;

  searchTerm.value = "";
  selectedCategory.value = "";
  selectedLocation.value = "";

  organisations.value = [];

  await loadRecommendations();
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 40px;
  background: #F6F2ED;
}

h1 {
  text-align: center;
  color: #2C2C2C;
  font-size: 3rem;
}

.subtitle {
  text-align: center;
  color: #777;
  margin-bottom: 40px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
}

@media (max-width: 900px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  color: #8B5A3C;
  border: 2px solid #8B5A3C;
  padding: 12px 18px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 25px;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: #8B5A3C;
  color: white;
  transform: translateX(-3px);
}
</style>
