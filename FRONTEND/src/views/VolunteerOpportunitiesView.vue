<script setup>
import { ref, onMounted } from "vue";
import VolunteerNeedCard from "@/components/VolunteerNeedCard.vue";
import { api } from "@/services/api";

const needs = ref([]);

onMounted(async () => {
  try {
    needs.value = await api.getVolunteerNeeds();
  } catch (error) {
    console.error(error);
  }
});

function signup(need) {
  console.log("Sign up for volunteer need:", need);
}
</script>

<template>
  <div class="container">
    <h1>Volunteer Opportunities</h1>
    <p class="text-muted">Charity volunteer needs and sign-up opportunities.</p>

    <div class="row g-3">
      <div v-for="need in needs" :key="need.volunteer_need_id" class="col-md-4">
        <VolunteerNeedCard :need="need" @signup="signup" />
      </div>
    </div>
  </div>
</template>
