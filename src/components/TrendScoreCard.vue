<!-- Purpose: Reusable card for displaying the trend score and trend status of an organisation. -->
<template>
  <!-- Reusable card for displaying the trend score and trend status of an organisation. -->
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">Trend Score</h5>
      <p class="display-6">{{ Number(trendScore || 0).toFixed(2) }}</p>
      <span class="badge bg-primary">{{ status || "Stable" }}</span>
    </div>
  </div>
</template>

<script setup>
// Reusable card for displaying the trend score and trend status of an organisation.
// trendScore and status are props so this card can be reused on dashboards and reports.
defineProps({
  trendScore: {
    type: Number,
    default: 0
  },
  status: {
    type: String,
    default: "Stable"
  }
});
</script>
