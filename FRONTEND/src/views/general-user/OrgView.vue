<template>

<div class="page">

  <button class="back-btn" @click="$router.back()">
    ← Back
  </button>

  <div v-if="loading">
    Loading organisation...
  </div>

  <div v-else>
    <div class="hero">
      <img
        class="hero-image"
        :src="organisation.image || 'https://placehold.co/500x300'"
        alt="Organisation"
        />
     </div>

    <div class="content">
      <!-- LEFT SIDE -->

    <div class="left">
      <div class="tags">
        <span>
          {{ organisation.organisation_type }}
         </span>

        <span v-if="organisation.category">
          {{ organisation.category_name }}
        </span>

      </div>

      <h1>
        {{ organisation.organisation_name }}
      </h1>

      <div class="rating">
        ⭐ 
        {{ organisation.rating || "No ratings yet" }}
      </div>

      <div class="location">
        📍
        {{
        organisation.address
        ?
        organisation.address
        :
        organisation.town && organisation.parish
        ?
        `${organisation.town}, ${organisation.parish}`
        :
        "Location unavailable"
        }}
      </div>

      <hr>

        <h2>
          About
        </h2>

        <p>
          {{ organisation.description }}
        </p>
      <hr>

      <h2>
         Reviews
      </h2>

      <div
        v-if="reviews.length"
      >

      <div
        class="review"
        v-for="review in reviews"
        :key="review.review_id"
      >

      <strong>
        ⭐ {{ review.rating }}
      </strong>

      <p>
        {{ review.review_text }}
      </p>

    </div>

   </div>

    <p v-else>
      No reviews yet.
    </p>

  </div>

  <!-- RIGHT SIDE -->
  <div class="sidebar">
    <div class="top-actions">
      <button class="save-btn" @click="saveOrganisation">
        ❤️ Save
      </button>

      <button 
        class="message-btn"
        @click="openMessages"
        >
          ✉
      </button>
    </div>
      <!-- BUSINESS ONLY -->
      <button
      v-if="organisation.organisation_type === 'business'"
      class="contact-btn"
      >
        Get in Touch
      </button>

      <!-- CHARITY ONLY -->
      <button
        v-if="organisation.organisation_type === 'charity'"
        class="donate-btn"
      >
        Donate
      </button>

      <div class="info">
        <h3>
          Contact
        </h3>

        <p>
          {{ organisation.phone || "No phone available" }}
        </p>

        <p>
          {{ organisation.email || "No email available" }}
        </p>

        <h3>
          Website
        </h3>

        <a
          v-if="organisation.website_url"
          :href="organisation.website_url"
          target="_blank"
        >
          {{ organisation.website_url }}
        </a>
        <p v-else>
          No website available
        </p>
      </div>
    </div>
  </div>
  </div>
</div>

</template>



<script setup>

import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { api } from "@/services/api";

const route = useRoute();
const organisation = ref({});
const reviews = ref([]);
const loading = ref(true);

onMounted(async()=>{
  try{
    organisation.value =
    await api.getOrganisation(
    route.params.id
  );
  // later this will come from reviews table
  reviews.value = organisation.value.reviews || [];

  }catch(error){
    console.error(error);
  }finally{
    loading.value = false;
  }
});

function saveOrganisation(){
  console.log(
    "Saved:", organisation.value.organisation_name
  );
}

function openMessages(){
    console.log(
        "Opening messages with:",
        organisation.value.organisation_name
    );
}

</script>

<style scoped>

.page{
  background:#F6F2ED;
  min-height:100vh;
  padding:30px 50px;
}

.back-btn{
  background:none;
  border:none;
  color:#8B5A3C;
  cursor:pointer;
  margin-bottom:30px;
  font-size:15px;
}

.hero{
  display:flex;
  justify-content:center;
  margin-bottom:40px;
}

.hero-image{
  width:420px;
  border-radius:15px;
  box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.content{
  display:grid;
  grid-template-columns:2fr 350px;
  gap:40px;
}

.left{
  background:white;
  padding:30px;
  border-radius:18px;
  box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.tags{
  display:flex;
  gap:10px;
  margin-bottom:15px;
}

.tags span{
  background:#EEE6DE;
  color:#8B5A3C;
  padding:6px 14px;
  border-radius:20px;
  font-size:13px;
}

h1{
  color:#2C2C2C;
  margin-bottom:10px;
}

.rating{
  color:#8B5A3C;
  margin-bottom:10px;
}

.location{
  color:#666;
  margin-bottom:20px;
}

h2{
  color:#2C2C2C;
  margin-top:25px;
}

p{
  line-height:1.7;
  color:#555;
}

.review{
  margin-top:20px;
  padding:15px;
  background:#FAFAFA;
  border-radius:10px;
}

.sidebar{
  align-self:start;
  position:sticky;
  top:30px;
  background:white;
  padding:25px;
  border-radius:18px;
  box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.top-actions{
  display:flex;
  gap:10px;
  margin-bottom:15px;
}

.save-btn{
  flex:1;
  padding:14px;
  border:none;
  border-radius:10px;
  background:#8B5A3C;
  color:white;
  cursor:pointer;
}

.message-btn{
  width:55px;
  border:none;
  border-radius:10px;
  background:white;
  color:#8B5A3C;
  font-size:22px;
  cursor:pointer;
  box-shadow:0 5px 15px rgba(0,0,0,.1);
}

.contact-btn,
.donate-btn{
  width:100%;
  padding:14px;
  margin-bottom:15px;
  border:none;
  border-radius:10px;
  background:#8B5A3C;
  color:white;
  cursor:pointer;
}

.save-btn:hover,
.contact-btn:hover,
.donate-btn:hover{
  background:#74482D;
}

.info{
  margin-top:20px;
}

.info h3{
  margin-bottom:5px;
  color:#2C2C2C;
}

.info a{
  color:#8B5A3C;
  text-decoration:none;
}

hr{
  margin:30px 0;
  border:none;
  border-top:1px solid #DDD;
}

@media(max-width:900px){
  .content{
    grid-template-columns:1fr;
}

.sidebar{
  position:relative;
}

.hero-image{
  width:100%;
  }

}

</style>