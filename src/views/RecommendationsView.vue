<!-- Purpose: Page-level screen for loading recommendation results for a selected user. -->
<script setup>
// Page-level screen for loading recommendation results for a selected user.
// userId is the test user whose recommendations will be loaded.
// recommendations stores the list returned by the recommendation API.
// loadRecommendations calls the backend and updates the page with the result.
import { ref } from "vue";
import RecommendationCard from "@/components/RecommendationCard.vue";
import { api } from "@/services/api";

const userId = ref(1);
const recommendations = ref([]);
const message = ref("");

async function loadRecommendations() {
  try {
    const result = await api.getRecommendations(userId.value);
    recommendations.value = result.recommendations || [];
    message.value = result.message || "";
  } catch (error) {
    message.value = error.message;
  }
}
</script>

<template>
  <!-- Page-level screen for loading recommendation results for a selected user. -->
  <div class="container">
    <h1>Recommended For You</h1>
    <p class="text-muted">Personalised recommendations based on ratings and user activity.</p>

    <div class="input-group mb-3">
      <span class="input-group-text">User ID</span>
      <input v-model="userId" class="form-control" type="number" />
      <button class="btn btn-primary" @click="loadRecommendations">Load</button>
    </div>

    <div v-if="message" class="alert alert-info">{{ message }}</div>

    <div class="row g-3">
      <div v-for="recommendation in recommendations" :key="recommendation.organisation_id" class="col-md-4">
        <RecommendationCard :recommendation="recommendation" />
      </div>
    </div>
  </div>
</template>
