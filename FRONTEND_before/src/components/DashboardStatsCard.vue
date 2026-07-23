<template>
  <div class="card text-center h-100">
    <div class="card-body">
      <p class="text-muted mb-1">{{ label }}</p>
      <h3>{{ value }}</h3>
    </div>
  </div>
</template>

<script setup>
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
