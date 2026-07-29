<template>

<div class="volunteer-page">

    <h2>Volunteer Opportunities</h2>
    <div
        v-if="loading"
    >
        Loading opportunities...
    </div>

    <div
        v-else-if="opportunities.length === 0"
        class="empty"
    >
        No volunteer opportunities available.
    </div>

    <div
        v-for="opportunity in opportunities"
        :key="opportunity.volunteer_need_id"
        class="opportunity-card"
    >
        <h3>
            {{ opportunity.title }}
        </h3>
        <p>
            <strong>
                Organisation:
            </strong>
            {{ opportunity.organisation_name }}
        </p>
        <p>
            {{ opportunity.description }}
        </p>
        <p>
            <strong>Date:</strong>
            {{ opportunity.needed_date }}
        </p>
        <p>
            <strong>Urgency:</strong>
            {{ opportunity.urgency_level }}
        </p>
        <p>
            <strong>Skills needed:</strong>
            {{
                opportunity.required_skills.join(", ")
            }}
        </p>
        <button
            @click="apply(opportunity.volunteer_need_id)"
        >
            {{
                applied.includes(opportunity.volunteer_need_id)
                ? "Request Sent"
                : "Volunteer"
            }}
        </button>
    </div>
</div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { api } from "@/services/api";

const opportunities = ref([]);
const loading = ref(false);
const applied = ref([]);

async function loadOpportunities(){
    try{
        loading.value = true;
        opportunities.value = await api.getVolunteerOpportunities();
    }
    catch(error){
        console.error(
            "Error loading opportunities",
            error
        );
    }finally{
        loading.value=false;
    }
}

async function apply(volunteerNeedId){
    try{
        const user =
            JSON.parse(
                localStorage.getItem("user")
            );

        await api.signupVolunteer({
            user_id:user.user_id,
            volunteer_need_id:volunteerNeedId
        });
        applied.value.push(volunteerNeedId);
    }catch(error){
        console.error(
            "Volunteer application failed",
            error
        );
    }
}

onMounted(()=>{
    loadOpportunities();
});

</script>


<style scoped>

.volunteer-page{
    display:grid;
    gap:20px;
}

.opportunity-card{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:
    0 5px 15px rgba(0,0,0,.1);
}

button{
    background:#965f3f;
    color:white;
    border:none;
    padding:10px 20px;
    border-radius:8px;
    cursor:pointer;
}
</style>