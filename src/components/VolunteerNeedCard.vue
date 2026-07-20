<!-- Purpose: Reusable card for displaying one volunteer need and emitting a signup action. -->
<template>
  <!-- Reusable card for displaying one volunteer need and emitting a signup action. -->
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">{{ need.title }}</h5>
      <p class="card-text">{{ need.description || "No description available." }}</p>
      <p class="mb-1"><strong>Urgency:</strong> {{ need.urgency_level }}</p>
      <p class="mb-3"><strong>Status:</strong> {{ need.status }}</p>
      <button class="btn btn-outline-primary btn-sm" @click="$emit('signup', need)">
        Sign Up
      </button>
    </div>
  </div>
</template>

<script setup>
// Reusable card for displaying one volunteer need and emitting a signup action.
// need is passed in from VolunteerOpportunitiesView.
// The signup event tells the parent which volunteer opportunity was selected.
defineProps({
  need: {
    type: Object,
    required: true
  }
});

defineEmits(["signup"]);
</script>
