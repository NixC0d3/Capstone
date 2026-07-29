<template>

    <div class="admin-page">

    <h1>Manage Users</h1>

        <div class="toolbar">
            <input
                v-model="search"
                placeholder="Search users..."
            />

            <select v-model="statusFilter">
                <option value="all">All Statuses</option>
                <option value="active">Active</option>
                <option value="spam">Spam</option>
                <option value="suspicious">Suspicious</option>
                <option value="inappropriate">Inappropriate</option>
            </select>
        
        </div>

        <table>

            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th></th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="user in filteredUsers" :key="user.user_id">

                    <td>{{user.first_name}} {{user.last_name}}</td>
                    <td>{{user.email}}</td>
                    <td>{{user.role}}</td>

                    <td>
                        <span :class="['status', user.status || 'active']">
                            {{ user.status || "active" }}
                        </span>
                    </td>

                    <td>
                        <button @click="viewUser(user.user_id)">
                            View
                        </button>
                    </td>

                </tr>

            </tbody>
            <tr v-if="filteredUsers.length === 0">
                <td colspan="5">
                    No users found.
                </td>
            </tr>

        </table>

    </div>

</template>

<script setup>
import {ref, onMounted, computed, watch} from "vue";
import {useRouter} from "vue-router";
import {api} from "@/services/api";

const router = useRouter();
const users = ref([]);
const search = ref("");
const statusFilter = ref("all");

async function loadUsers(status = "all") {
    try {
        users.value = await api.getUsers(status);
    } catch (error) {
        console.error("Failed loading users:", error);
    }
}

onMounted(async () => {
    await loadUsers();
});

watch(statusFilter, async(newStatus) => {
    await loadUsers(newStatus);
});

const filteredUsers = computed(() => {
    return users.value.filter(user => {
        return `${user.first_name} ${user.last_name} ${user.email}`
            .toLowerCase()
            .includes(search.value.toLowerCase());
    });
});

function viewUser(id){
    router.push(`/admin/users/${id}`);
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

.status{
    display:inline-block;
    padding:5px 12px;
    border-radius:20px;
    color:white;
    font-size:13px;
    font-weight:bold;
    text-transform:capitalize;
}

.status.active{
    background:#28a745;
}

.status.spam{
    background:#dc3545;
}

.status.suspicious{
    background:#fd7e14;
}

.status.inappropriate{
    background:#6f42c1;
}

</style>