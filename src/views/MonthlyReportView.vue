<!-- Purpose: Page-level view used to demonstrate the trend score/monthly report calculation. -->
<script setup>
// Page-level view used to demonstrate the trend score/monthly report calculation.
// result stores the calculated trend score returned from the Flask API.
// calculateDemoReport sends sample engagement values to test the trend score endpoint.
import { ref } from "vue";
import TrendScoreCard from "@/components/TrendScoreCard.vue";
import { api } from "@/services/api";

const result = ref(null);

async function calculateDemoReport() {
  result.value = await api.calculateTrendScore({
    total_reviews: 10,
    total_rating_score: 43,
    global_average_rating: 4.0,
    previous_trend_score: 75,
    engagement_counts: {
      profile_views: 100,
      saves: 20,
      messages: 10,
      ratings: 10,
      volunteer_signups: 5
    }
  });
}
</script>

<template>
  <!-- Page-level view used to demonstrate the trend score/monthly report calculation. -->
  <div class="container">
    <h1>Monthly Report</h1>
    <p class="text-muted">Trend score and monthly performance report for an organisation.</p>

    <button class="btn btn-primary mb-3" @click="calculateDemoReport">
      Calculate Demo Report
    </button>

    <TrendScoreCard
      v-if="result"
      :trend-score="result.trend_score"
      :status="result.trend_status"
    />

    <pre v-if="result" class="mt-3 bg-light p-3 rounded">{{ result }}</pre>
  </div>
</template>
