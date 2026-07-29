<template>

<div
  class="charity-card"
  @click="openCharity"
>
    <span 
    v-if="charity.organisation_type === 'charity'"
    class="category"
    >
        {{ charity.category_name}}
    </span>

    <div class="header">
        <h2>
            {{ charity.organisation_name }}
        </h2>

        <span class="heart">
            {{ charity.is_saved ? "♥" : "♡" }}
        </span>
    </div>

    <div class="rating">
        ⭐ {{ charity.rating || "No ratings yet" }}
    </div>

    <p class="location">
        📍 
        {{ charity.town && charity.parish 
            ? `${charity.town}, ${charity.parish}` 
            : "Location unavailable"
        }}
    </p>

    <p class="description">
        {{ charity.description }}
    </p>

    <div class="actions">

        <button class="donate">
            Donate
        </button>

        <button
          class="learn-more-btn"
          @click.stop="openCharity"
        >
          Learn More
        </button>
    </div>

</div>

</template>


<script setup>

import { useRouter } from "vue-router";
import { api } from "@/services/api";

const router = useRouter();

const props = defineProps({
  charity: {
    type: Object,
    required: true
  }
});

async function openCharity() {
  try {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const userId = user.user_id || user.id;

    if (userId && props.charity?.organisation_id) {
      await api.logEngagement({
        organisation_id: props.charity.organisation_id,
        user_id: userId,
        engagement_type: "profile_view"
      });
    }
  } catch (error) {
    console.error("Failed to log profile view:", error);
  }

  router.push(`/generaluser/organisation/${props.charity.organisation_id}`);
}

</script>


<style scoped>

.charity-card{
    background:white;
    width:600px;
    padding:30px;
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    margin-bottom:25px;
}

.category{
    font-size:13px;
    color:#8B5A3C;
    text-transform:uppercase;
}

h2{
    margin:10px 0;
    color:#2C2C2C;
}

.rating{
    margin-bottom:10px;
}

.location{
    color:#666;
}


.description{
    color:#555;
    line-height:1.5;
}


.actions{
    display:flex;
    gap:15px;
    margin-top:20px;
}


button{
    padding:12px 25px;
    border-radius:10px;
    cursor:pointer;
}


.donate{
    background:#8B5A3C;
    color:white;
    border:none;
}

.learn{
    background:white;
    color:#8B5A3C;
    border:2px solid #8B5A3C;
}

@media(max-width:700px){
    .charity-card{
        width:auto;
    }
}
.header{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.heart{
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
</style>
