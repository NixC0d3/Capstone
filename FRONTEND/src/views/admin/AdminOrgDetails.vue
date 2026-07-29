<template>
  <div class="admin-page" v-if="organisation">

    <div class="header">
      <h1>{{ organisation.organisation_name }}</h1>
      <span class="status">
        {{ formatType(organisation.organisation_type) }}
      </span>
    </div>

    <div class="card">

      <h2>Organisation Information</h2>

      <div class="info-row">
        <span class="label">Email</span>
        <span>{{ organisation.email || "N/A" }}</span>
      </div>

      <div class="info-row">
        <span class="label">Phone</span>
        <span>{{ organisation.phone || "N/A" }}</span>
      </div>

      <div class="info-row">
        <span class="label">Website</span>
        <span>{{ organisation.website_url || "N/A" }}</span>
      </div>

    </div>

    <div class="card">

      <h2>Location</h2>

      <div class="info-row">
        <span class="label">Town</span>
        <span>{{ organisation.location?.town || "N/A" }}</span>
      </div>

      <div class="info-row">
        <span class="label">Parish</span>
        <span>{{ organisation.location?.parish || "N/A" }}</span>
      </div>

    </div>

    <div class="card">

      <h2>Description</h2>

      <p>
        {{ organisation.description || "No description available." }}
      </p>

    </div>

    <div class="card">

      <h2>Categories</h2>

      <div class="tags">

        <span
            v-if="organisation.category"
            class="tag"
        >
            {{ organisation.category }}
        </span>

        <span v-else>
          No categories assigned.
        </span>

      </div>

    </div>

    <div class="card">

      <h2>Owner</h2>

      <div class="info-row">
        <span class="label">Name</span>
        <span>{{ organisation.owner?.name || "N/A" }}</span>
      </div>

    </div>

    <div class="actions">

      <button class="warning">
        Deactivate
      </button>

      <button class="danger">
        Delete
      </button>

      <button @click="router.back()">
        Back
      </button>

    </div>

  </div>

  <div v-else>
    Loading organisation...
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "@/services/api";

const route = useRoute();
const router = useRouter();

const organisation = ref(null);

async function loadOrganisation() {
  try {
    organisation.value = await api.getAdminOrganisation(
      route.params.id
    );
  } catch (error) {
    console.error(error);
  }
}

function formatType(type) {
  if (type === "business") return "Business";
  if (type === "charity") return "Charity";
  return type;
}

onMounted(() => {
  loadOrganisation();
});
</script>

<style scoped>
.admin-page{
    max-width:900px;
    margin:auto;
    padding:40px;
    background:#F6F2ED;
    min-height:100vh;
}

.header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:30px;
}

.status{
    background:#d8f3dc;
    color:#2d6a4f;
    padding:8px 14px;
    border-radius:20px;
    font-weight:bold;
}

.card{
    background:white;
    border-radius:15px;
    padding:25px;
    margin-bottom:25px;
    box-shadow:0 5px 15px rgba(0,0,0,.08);
}

h2{
    margin-bottom:20px;
    color:#8B5A3C;
}

.info-row{
    display:flex;
    justify-content:space-between;
    padding:10px 0;
    border-bottom:1px solid #eee;
}

.label{
    font-weight:bold;
}

.tags{
    display:flex;
    flex-wrap:wrap;
    gap:10px;
}

.tag{
    background:#EFE5DB;
    color:#8B5A3C;
    padding:8px 14px;
    border-radius:999px;
}

.actions{
    display:flex;
    gap:15px;
    margin-top:30px;
}

button{
    padding:10px 20px;
    border:none;
    border-radius:8px;
    cursor:pointer;
}

.warning{
    background:#f4a261;
    color:white;
}

.danger{
    background:#d62828;
    color:white;
}

button:last-child{
    background:#8B5A3C;
    color:white;
}
</style>