<template>
  <div class="page">
    <h1>Create {{ organisationType === "business" ? "Business" : "Charity" }}</h1>

    <OrganisationForm
      :organisation="organisation"
      :categories="categories"
      :locations="locations"
      @submit="createOrganisation"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { api } from "@/services/api";
import OrganisationForm from "@/components/OrganisationForm.vue";

const router = useRouter();

const categories = ref([]);
const locations = ref([]);

const props = defineProps({
    organisationType:{
        type:String,
        required:true
    }
});

const organisation = ref({
  organisation_name: "",
  description: "",
  category_id: "",
  location_id: "",
  phone: "",
  email: "",
  website_url: ""
});

onMounted(async () => {
  categories.value = await api.getCategories();
  locations.value = await api.getLocations();
});

async function createOrganisation(formData) {
  try {
    const user = JSON.parse(localStorage.getItem("user"));

    await api.createOrganisation({
      ...formData,
      owner_user_id: user.user_id,
      organisation_type: props.organisationType
    });

    alert(`${props.organisationType} created successfully!`);

    if(props.organisationType === "business"){
        router.push("/business-user/home");
    }
    else{
        router.push("/charity-user/home");
    }

  } catch (error) {
    console.error(error);
    alert(`Failed to create ${props.organisationType}.`);
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