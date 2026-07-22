<template>
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">Trend Score</h5>
      <p class="display-6">{{ Number(trendScore || 0).toFixed(2) }}</p>
      <span class="badge bg-primary">{{ status || "Stable" }}</span>
    </div>
  </div>
</template>

<script setup>
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
