<template>
  <form class="organisation-form" @submit.prevent="submitForm">

    <div class="form-group">
      <label>Organisation Name</label>
      <input
        v-model="form.organisation_name"
        type="text"
        required
      />
    </div>

    <div class="form-group">
      <label>Description</label>
      <textarea
        v-model="form.description"
        rows="5"
      ></textarea>
    </div>

    <div class="form-group">
      <label>Category</label>
      <select v-model="form.category_id">
        <option disabled value="">Select a category</option>

        <option
          v-for="category in categories"
          :key="category.category_id"
          :value="category.category_id"
        >
          {{ category.category_name }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label>Parish</label>
      <select v-model="form.parish">
        <option disabled value="">Select parish</option>

        <option
          v-for="location in locations"
          :key="location.location_id"
          :value="location.parish"
        >
          {{ location.parish }}
        </option>
      </select>
    </div>
    <div class="form-group">
      <label>Town</label>
      <input
        v-model="form.town"
        type="text"
      />
    </div>

    <div class="form-group">
      <label>Street Address</label>
      <input
        v-model="form.address"
        type="text"
      />
    </div>

    <div class="form-group">
      <label>Phone</label>
      <input
        v-model="form.phone"
        type="text"
      />
    </div>

    <div class="form-group">
      <label>Email</label>
      <input
        v-model="form.email"
        type="email"
      />
    </div>

    <div class="form-group">
      <label>Website</label>
      <input
        v-model="form.website_url"
        type="url"
        placeholder="https://example.com"
      />
    </div>

    <button class="save-btn" type="submit">
      Save Organisation
    </button>

  </form>
</template>

<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  organisation: {
    type: Object,
    required: true
  },

  categories: {
    type: Array,
    default: () => []
  },
  locations:{
    type:Array,
    default:()=>[]
  }
});

const emit = defineEmits([
  "submit"
]);

const form = reactive({
  organisation_name: "",
  description: "",
  category_id: "",
  parish: "",
  town: "",
  address: "",
  phone: "",
  email: "",
  website_url: ""
});

watch(
  () => props.organisation,
  (value) => {
    Object.assign(form, {
      organisation_name: value.organisation_name || "",
      description: value.description || "",
      category_id: value.category_id || "",
      parish: value.parish || "",
      town: value.town || "",
      address: value.address || "",
      phone: value.phone || "",
      email: value.email || "",
      website_url: value.website_url || ""
    });
  },
  {
    immediate: true
  }
);

function submitForm() {
  emit("submit", {
    ...form
  });
}
</script>

<style scoped>

.organisation-form{
    display:flex;
    flex-direction:column;
    gap:20px;
    max-width:700px;
    margin:auto;
    padding:30px;
    background:white;
    border-radius:18px;
    box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.form-group{
    display:flex;
    flex-direction:column;
    gap:8px;
}

label{
    font-weight:600;
    color:#333;
}

input,
textarea,
select{
    padding:12px;
    border:1px solid #ddd;
    border-radius:10px;
    font-size:15px;
    font-family:inherit;
}

textarea{
    resize:vertical;
}

input:focus,
textarea:focus,
select:focus{
    outline:none;
    border-color:#8B5A3C;
}

.save-btn{
    margin-top:10px;
    padding:14px;
    border:none;
    border-radius:10px;
    background:#8B5A3C;
    color:white;
    font-size:16px;
    cursor:pointer;
}

.save-btn:hover{
    background:#74482D;
}

</style>