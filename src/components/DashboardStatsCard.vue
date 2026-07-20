<!-- Purpose: Small reusable card for displaying one dashboard statistic. -->
<template>
  <!-- Small reusable card for displaying one dashboard statistic. -->
  <div class="card text-center h-100">
    <div class="card-body">
      <p class="text-muted mb-1">{{ label }}</p>
      <h3>{{ value }}</h3>
    </div>
  </div>
</template>

<script setup>
// Small reusable card for displaying one dashboard statistic.
// label and value are props, so this card can be reused for different dashboard numbers.
defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    default: 0
  }
});
</script>
