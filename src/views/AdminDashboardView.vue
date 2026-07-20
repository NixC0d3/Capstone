<!-- Purpose: Page-level view for admin controls, including trend score weights. -->
<script setup>
// Page-level view for admin controls, including trend score weights.
// settings stores the admin-controlled trend score weights from the backend.
// saveSettings sends updated weights back to the Flask API.
import { ref, onMounted } from "vue";
import { api } from "@/services/api";

const settings = ref({});

onMounted(async () => {
  try {
    settings.value = await api.getEngagementWeights();
  } catch (error) {
    console.error(error);
  }
});

async function saveSettings() {
  try {
    settings.value = await api.updateEngagementWeights(settings.value);
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <!-- Page-level view for admin controls, including trend score weights. -->
  <div class="container">
    <h1>Admin Dashboard</h1>
    <p class="text-muted">Admin-controlled weights for the trend score algorithm.</p>

    <div class="card card-body">
      <div v-for="(value, key) in settings" :key="key" class="mb-3">
        <label class="form-label">{{ key }}</label>
        <input v-model.number="settings[key]" class="form-control" type="number" step="0.1" />
      </div>

      <button class="btn btn-primary" @click="saveSettings">Save Settings</button>
    </div>
  </div>
</template>
