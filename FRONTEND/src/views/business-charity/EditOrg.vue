<template>
  <div class="page">

    <h1>Edit {{ organisationType === "business" ? "Business" : "Charity" }}</h1>

    <div v-if="loading">
      Loading...
    </div>

    <OrganisationForm
      v-else
      :organisation="organisation"
      :categories="categories"
      :locations="locations"
      @submit="updateOrganisation"
    />

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "@/services/api";
import OrganisationForm from "@/components/OrganisationForm.vue";

const loading = ref(true);
const organisation = ref({});
const categories = ref([]);
const locations = ref([]);

const props = defineProps({
    organisationType:{
        type:String,
        required:true
    }
});

onMounted(async () => {
  try {
    const user = JSON.parse(localStorage.getItem("user"));

    organisation.value = await api.getOwnerOrganisation(user.user_id);
    categories.value = await api.getCategories();
    locations.value = await api.getLocations();
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
});

async function updateOrganisation(formData) {
  try {

    await api.updateOrganisation(
      organisation.value.organisation_id,
      formData
    );
    alert(`${props.organisationType} updated successfully!`);

  } catch (error) {
    console.error(error);
    alert("Failed to update business.");
  }
}
</script>

<style scoped>
.page{
    padding:40px;
    background:#F6F2ED;
    min-height:100vh;
}

h1{
    text-align:center;
    color:#8B5A3C;
    margin-bottom:30px;
}
</style>