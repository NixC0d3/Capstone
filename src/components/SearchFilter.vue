<!-- Purpose: Reusable search/filter form for filtering organisations by search text and organisation type. -->
<template>
  <!-- When submitted, this form sends the filter values to its parent component. -->
  <form class="row g-2 mb-4" @submit.prevent="submitSearch">
    <div class="col-md-5">
      <input v-model="searchTerm" class="form-control" placeholder="Search businesses or charities" />
    </div>

    <div class="col-md-4">
      <select v-model="organisationType" class="form-select">
        <option value="">All types</option>
        <option value="business">Businesses</option>
        <option value="charity">Charities</option>
      </select>
    </div>

    <div class="col-md-3">
      <button class="btn btn-primary w-100">Search</button>
    </div>
  </form>
</template>

<script setup>
// Reusable search/filter form for filtering organisations by search text and organisation type.
// This component does not filter by itself. It emits the search values to its parent page.
// searchTerm and organisationType are connected to the input/select using v-model.
import { ref } from "vue";

const emit = defineEmits(["search"]);

const searchTerm = ref("");
const organisationType = ref("");

function submitSearch() {
  emit("search", {
    searchTerm: searchTerm.value,
    organisationType: organisationType.value
  });
}
</script>
