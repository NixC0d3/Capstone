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
            <span>
                {{ organisation.category_name }}
            </span>
        </div>

        <div class="rating">
            ⭐ {{ organisation.rating || "No ratings yet" }}
        </div>

        <p class="location">
            📍 
            {{
                organisation.address || organisation.town || organisation.parish
                || "Location unavailable"
            }}
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

const displayCategories = computed(() => {
  if (props.organisation.categories && props.organisation.categories.length > 0) {
    return props.organisation.categories
      .map(category => category.category_name)
      .join(", ");
  }

  return props.organisation.category_name || "Uncategorized";
});

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
