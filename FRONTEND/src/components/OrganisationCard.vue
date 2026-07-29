<template>

<div 
class="card"
@click="openOrganization"
>
    <!-- Image -->
    <img
        :src="organisation.image || 'https://placehold.co/300x200'"
        class="org-image"
    />

    <div class="card-content">
        <div class="header">
            <h3>
                {{ organisation.organisation_name }}
            </h3>

            <span class="heart">
                {{ organisation.is_saved === true ? "♥" : "♡" }}
            </span>
        </div>


        <div class="tags">
          <span
            v-for="category in displayCategoryList"
            :key="category"
          >
            {{ category }}
          </span>
        </div>

        <div class="rating">
            ⭐ {{ organisation.rating || "No ratings yet" }}
        </div>

        <p class="location">
          📍 {{ formatLocation(organisation) }}
        </p>

        <p class="description">
            {{ organisation.description }}
        </p>

    </div>
</div>
</template>

<script setup>
import { useRouter } from "vue-router"
import { computed } from "vue";

const router = useRouter()

const props = defineProps({
    organisation: {
        type: Object,
        required: true
    }
});

const displayCategoryList = computed(() => {
  const categoryNames = [];

  if (props.organisation.category_name) {
    categoryNames.push(props.organisation.category_name);
  }

  if (props.organisation.categories && props.organisation.categories.length > 0) {
    props.organisation.categories.forEach(category => {
      if (category.category_name) {
        categoryNames.push(category.category_name);
      }
    });
  }

  // Remove duplicates
  const uniqueCategories = [...new Set(categoryNames)];

  if (uniqueCategories.length === 0) {
    return ["Uncategorized"];
  }

  return uniqueCategories;
});

function formatLocation(organisation) {
  const parts = [];

  // 1. Parish first
  if (organisation.parish) {
    parts.push(organisation.parish);
  }

  // 2. Town second
  if (organisation.town) {
    parts.push(organisation.town);
  }

  // 3. Road/address last
  if (organisation.address) {
    parts.push(organisation.address);
  }

  if (parts.length === 0) {
    return "Location unavailable";
  }

  return parts.join(", ");
}

function openOrganization() {
    router.push(`/organisation/${props.organisation.organisation_id}`)
}
function saveOrg() {
    console.log("Saved:", props.organisation.organisation_name);
}
</script>


<style scoped>

.card{
    background:white;
    padding:25px;
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}


h3{
    color:#2C2C2C;
}

p{
    color:#666;
}
.description{
    height:75px;
    overflow:hidden;
    display:-webkit-box;
    -webkit-line-clamp:3;
    -webkit-box-orient:vertical;
    text-overflow:ellipsis;
}
.heart {
    display:flex;
    align-items:center;
    justify-content:center;
    width:42px;
    height:42px;
    background:#8B5A3C;
    color:white;
    border-radius:10px;
    font-size:20px;
}
.header{
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    margin-bottom:10px;
}
.tags{
    display:flex;
    gap:8px;
    margin-bottom:15px;
}
.tags span{
    background:#EEE6DE;
    color:#8B5A3C;
    padding:5px 12px;
    border-radius:20px;
    font-size:12px;
}

</style>
