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

    <div v-if="hasSearched">
        <button class="back-button" @click="goBack">
            ← Clear Search
        </button>

      <h2>Search Results</h2>

      <div v-if="filteredOrganisations.length" class="card-grid">
        <OrganisationCard
            v-for="org in filteredOrganisations"
            :key="org.organisation_id"
            :organisation="org"
        />
      </div>

      <p v-else>
        No organisations match your search.
      </p>

    </div>

    <div v-else>
      <h2>Recommended for you</h2>
      <div class="card-grid">
        <OrganisationCard
          v-for="org in organisations"
          :key="org.organisation_id"
          :organisation="org"
        />
      </div>

    </div>

  </div>
</template>

<script setup>

import { ref, computed, onMounted } from "vue";

import SearchBar from "@/components/SearchBar.vue";
import OrganisationCard from "@/components/OrganisationCard.vue";

import { api } from "@/services/api";


const organisations = ref([]);
const categories = ref([]);
const locations = ref([]);

const searchTerm = ref("");
const selectedCategory = ref("");
const selectedLocation = ref("");

const hasSearched = ref(false);


/*
    GET ORGANISATIONS FROM DATABASE
*/
onMounted(async () => {
  try {

    const organisationResponse = await api.getOrganisations({type: "busines"});
    organisations.value = organisationResponse;

    categories.value = await api.getCategories();
    locations.value = await api.getLocations();

  } catch(error){
    console.error(error);
  }
});


/*
    FILTER DATABASE RESULTS
*/
const filteredOrganisations = computed(() => {
  return organisations.value.filter(org => {
    const name =
      (
        org.organisation_name || ""
      ).toLowerCase();
    const category =
      (
        org.category_name || ""
      ).toLowerCase();
    const location =
      (
        org.parish || ""
      ).toLowerCase();

      const matchesSearch = name.includes(
        searchTerm.value.toLowerCase()
      );
      const matchesCategory = !selectedCategory.value || category === selectedCategory.value.toLowerCase();

      const matchesLocation = !selectedLocation.value || location === selectedLocation.value.toLowerCase();
  
      return (
        matchesSearch &&
        matchesCategory &&
        matchesLocation
      );
  });
});

function searchOrganizations(){
  hasSearched.value = true;
}

function goBack(){
  hasSearched.value = false;
  searchTerm.value = "";
  selectedCategory.value = "";
  selectedLocation.value = "";
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