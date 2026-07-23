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

            <button
            class="heart"
            @click.stop="saveOrg"
            >
            ♡
            </button>
        </div>


        <div class="category">
            {{ organisation.category_name }}
        </div>

        <div class="rating">
            ⭐ {{ organisation.rating || "No ratings yet" }}
        </div>

        <p class="location">
            📍 
            {{
                organisation.town && organisation.parish
                ? `${organisation.town}, ${organisation.parish}`
                : "Location unavailable"
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
const router = useRouter()

const props = defineProps({
    organisation: {
        type: Object,
        required: true
    }
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
    min-height:50px;
}

button{
    background:#8B5A3C;
    color:white;
    border:none;
    padding:10px 20px;
    border-radius:10px;
}

</style>