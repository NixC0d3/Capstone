<template>
  <div class="card h-100 border-success">
    <div class="card-body">
      <h5 class="card-title">Recommended Organisation #{{ recommendation.organisation_id }}</h5>
      <p class="card-text">
        Predicted score:
        <strong>{{ Number(recommendation.predicted_score || 0).toFixed(2) }}</strong>
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  recommendation: {
    type: Object,
    required: true
  }
});
</script>
