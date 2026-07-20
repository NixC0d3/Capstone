<!-- Purpose: Reusable card for showing one business or charity in a list/grid. -->
<template>
  <!-- Displays basic organisation data inside a reusable Bootstrap card. -->
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">{{ organisation.organisation_name || organisation.name || "Organisation" }}</h5>
      <p class="card-text text-muted">{{ organisation.organisation_type || "business/charity" }}</p>
      <p class="card-text">{{ organisation.description || "No description available yet." }}</p>
      <RouterLink
        v-if="organisation.organisation_id"
        class="btn btn-primary btn-sm"
        :to="`/organisations/${organisation.organisation_id}`"
      >
        View Details
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
// Reusable card for showing one business or charity in a list/grid.
// organisation is passed in from a parent view such as ExploreView.
import { RouterLink } from "vue-router";

defineProps({
  organisation: {
    type: Object,
    required: true
  }
});
</script>
