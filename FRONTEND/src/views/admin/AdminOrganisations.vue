<template>

    <div class="admin-page">

    <h1>Manage Organisations</h1>

        <div class="toolbar">
            <input
                v-model="search"
                placeholder="Search organisations..."
            />      
        
            <select v-model="typeFilter">
                <option value="all">
                    All Types
                </option>

                <option value="business">
                    Business
                </option>

                <option value="charity">
                    Charity
                </option>
            </select>
        </div>
        <table>

            <thead>
                <tr>
                    <th>Organisation</th>
                    <th>Owner</th>
                    <th>Type</th>
                    <th></th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="org in filteredOrganisations" :key="org.organisation_id">

                    <td>{{org.organisation_name}}</td>
                    <td>{{org.owner}}</td>
                    <td>{{ formatType(org.organisation_type) }}</td>

                    <td>
                        <button @click="viewOrganisation(org.organisation_id)">
                            View
                        </button>
                    </td>

                </tr>

            </tbody>
            <tr v-if="filteredOrganisations.length === 0">
                <td colspan="4">
                    No organisations found.
                </td>
            </tr>

        </table>

    </div>

</template>

<script setup>
import {ref, onMounted, computed} from "vue";
import {useRouter} from "vue-router";
import {api} from "@/services/api";

const router = useRouter();
const organisations = ref([]);
const search = ref("");
const typeFilter = ref("all");
async function loadOrganisations() {
    try {
        organisations.value = await api.getAdminOrganisations();;
    } catch(error) {
        console.error("Failed loading organisations:", error);
    }
}

onMounted(async () => {
    await loadOrganisations();
});


const filteredOrganisations = computed(() => {
    return organisations.value.filter(org => {
        const searchMatch =
            `${org.organisation_name}`
            .toLowerCase()
            .includes(search.value.toLowerCase());
        const typeMatch =
            typeFilter.value === "all" ||
            org.organisation_type === typeFilter.value

        return searchMatch && typeMatch;
    });
});

function formatType(type){
    if(type === "business"){
        return "Business";
    }
    if(type === "charity"){
        return "Charity";
    }
    return type;
}

function viewOrganisation(id){
    router.push(`/admin/organisations/${id}`);
}
</script>

<style scoped>

.admin-page{
    padding:40px;
    background:#F6F2ED;
    min-height:100vh;
}

h1{
    color:#8B5A3C;
}

.toolbar{
    display:flex;
    gap:20px;
    margin-bottom:30px;
    align-items:center;
}

input,
select{
    padding:12px;
    border-radius:8px;
    border:1px solid #ccc;
}

table{
    width:100%;
    background:white;
    border-radius:15px;
    overflow:hidden;
    border-collapse:collapse;
}

th,
td{
    padding:15px;
    text-align:left;
    border-bottom:1px solid #eee;
}

button{
    background:#8B5A3C;
    color:white;
    border:none;
    padding:10px 15px;
    border-radius:8px;
    cursor:pointer;
}

button:hover{
    opacity:.9;
}


</style>