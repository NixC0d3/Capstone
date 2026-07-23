<template>

<div class="dashboard">

    <h1>
        Support Your Community
    </h1>
    <p class="subtitle">
        Discover charities making a difference
    </p>

    <SearchBar
        @search="searchCharities"
    />

    <div v-if="hasSearched">

        <h2>
            Search Results
        </h2>

        <div v-if="searchResults.length" class="charity-list">

            <CharityCard
                v-for="charity in searchResults"
                :key="charity.id"
                :charity="charity"
            />

        </div>
        <p v-else>
            No charities found.
        </p>

    </div>

    <div v-else>
        <h2>
            Recommended Charities
        </h2>

        <div class="charity-list">
            <CharityCard
                v-for="charity in charities"
                :key="charity.organisation_id"
                :charity="charity"
            />

        </div>

    </div>

</div>

</template>

<script setup>

import { ref, onMounted } from "vue";

import SearchBar from "@/components/SearchBar.vue";
import CharityCard from "@/components/CharityCard.vue";
import { api } from "@/services/api";

const charities = ref([]);
const searchResults = ref([]);
const hasSearched = ref(false);


function searchCharities(filters){
    hasSearched.value = true;

    searchResults.value =
    charities.value.filter(charity=>{

        const matchesName =
        charity.organisation_name
        .toLowerCase()
        .includes(filters.searchTerm.toLowerCase());

        const matchesCategory =
        !filters.category ||
        charity.category_name === filters.category;

        const matchesLocation =
        !filters.location ||
        charity.parish === filters.location;

        return matchesName 
        && matchesCategory 
        && matchesLocation;
    });
}

onMounted(async()=>{
    try{
        const organisations = await api.getOrganisations();
        charities.value = organisations.filter(
            organisation =>
            organisation.organisation_type === "charity"
        );
    }catch(error){
        console.error(error);
    }
});


</script>



<style scoped>
.dashboard{
    min-height:100vh;
    padding:40px;
    background:#F6F2ED;
}

h1{
    text-align:center;
    font-size:3rem;
    color:#2C2C2C;
}

.subtitle{
    text-align:center;
    color:#777;
    margin-bottom:40px;
}

.charity-list{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:30px;
}

@media(max-width:900px){
    .charity-list{
        grid-template-columns:1fr;
    }
}

h2{
    margin-top:40px;
    margin-bottom:25px;
    color:#2C2C2C;
}
</style>