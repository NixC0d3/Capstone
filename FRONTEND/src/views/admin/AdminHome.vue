<template>

<div class="admin-page">
    <h1>Admin Dashboard</h1>

    <div class="cards">
        <div class="card">
            <h2>General Users</h2>
            <p>{{ usersCount }}</p>
            <button @click="router.push('/admin/users')">
                Manage Users
            </button>
        </div>

        <div class="card">
            <h2>Organisations</h2>
            <p>{{ organisationCount }}</p>
            <button @click="router.push('/admin/organisations')">
                Manage Organisations
            </button>
        </div>

        <div class="card">
            <h2>Trend Score Settings</h2>
            <p>
                Configure scoring weights
            </p>
            <button>
                Edit Settings
            </button>
        </div>
    </div>

</div>

</template>


<script setup>

import {ref,onMounted} from "vue";
import {api} from "@/services/api";
import { useRouter } from "vue-router";

const router = useRouter();

const usersCount = ref(0);
const organisationCount = ref(0);

onMounted(async()=>{
    try{
        const users = await api.getUsers();
        usersCount.value = users.length;

        const organisations = await api.getOrganisations();
        organisationCount.value = organisations.length;
    }
    catch(error){
        console.error(
            "Failed loading admin dashboard",
            error
        );
    }
});

</script>


<style scoped>

.admin-page{
    padding:40px;
    background:#F6F2ED;
    min-height:100vh;
}

h1{
    color:#8B5A3C;
    margin-bottom:30px;
}

.cards{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:30px;
}

.card{
    background:white;
    padding:30px;
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}

.card h2{
    color:#8B5A3C;
}
.card p{
    font-size:30px;
    font-weight:bold;
}

button{
    background:#8B5A3C;
    color:white;
    border:none;
    padding:12px 20px;
    border-radius:10px;
    cursor:pointer;
}

</style>