<!-- Purpose: Page-level view for listing, searching, and filtering organisations. -->
<script setup>
// Page-level view for listing, searching, and filtering organisations.
// organisations stores the data loaded from the Flask API.
// filters stores the current search and type filter selected by the user.
// onMounted runs once when this page opens and loads organisation data from the backend.
// filteredOrganisations is recalculated automatically when organisations or filters change.
import { ref, computed, onMounted } from "vue";
import SearchFilter from "@/components/SearchFilter.vue";
import OrganisationCard from "@/components/OrganisationCard.vue";
import { api } from "@/services/api";

const organisations = ref([]);
const filters = ref({ searchTerm: "", organisationType: "" });

onMounted(async () => {
  try {
    organisations.value = await api.getOrganisations();
  } catch (error) {
    console.error(error);
  }
});

const filteredOrganisations = computed(() => {
  return organisations.value.filter((organisation) => {
    const name = (organisation.organisation_name || "").toLowerCase();
    const matchesSearch = name.includes(filters.value.searchTerm.toLowerCase());
    const matchesType =
      !filters.value.organisationType ||
      organisation.organisation_type === filters.value.organisationType;

    return matchesSearch && matchesType;
  });
});

function updateFilters(newFilters) {
  filters.value = newFilters;
}
</script>

<template>
  <!-- SearchFilter controls the filters, and OrganisationCard displays each matching result. -->
  <div class="container">
    <h1>Explore Organisations</h1>
    <p class="text-muted">Search and filter businesses and charities.</p>

    <SearchFilter @search="updateFilters" />

    <div class="row g-3">
      <div v-for="organisation in filteredOrganisations" :key="organisation.organisation_id" class="col-md-4">
        <OrganisationCard :organisation="organisation" />
      </div>
    </div>
  </div>
</template>
