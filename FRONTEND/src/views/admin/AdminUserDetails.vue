<template>
    <div class="page">
    
        <h1>User Details</h1>

        <div v-if="user">
            <div class="card">
                <h2>
                    {{user.first_name}}
                    {{user.last_name}}
                </h2>

                <p>
                    Email: {{user.email}}
                </p>

                <p>
                    Role: {{user.role}}
                </p>
                <p>
                    Status: {{user.status}}
                </p>
            </div>


            <div class="card">
                <h2>
                    Activity
                </h2>

                <p>
                    Organisations: {{activity.organisations}}
                </p>

                <p>
                    Reviews: {{activity.reviews}}
                </p>

                <p>
                    Messages: {{activity.messages}}
                </p>

                <p>
                    Saved: {{activity.saved}}
                </p>
            </div>

            <div class="card">

                <h2>
                    Moderation History
                </h2>

                <table v-if="moderationHistory.length">

                    <thead>
                        <tr>
                            <th>Status</th>
                            <th>Notes</th>
                            <th>Date</th>
                        </tr>
                    </thead>

                    <tbody>

                        <tr 
                        v-for="item in moderationHistory"
                        :key="item.date"
                        >

                            <td>
                                {{item.reason}}
                            </td>

                            <td>
                                {{item.notes}}
                            </td>

                            <td>
                                {{item.date}}
                            </td>

                        </tr>

                    </tbody>

                </table>

                <p v-else>
                    No moderation history
                </p>

            </div>

            <div class="card">
            <h2>
                Admin Decision
            </h2>
            <button
                @click="review('inappropriate')"
                >
                Inappropriate
            </button>


            <button
                @click="review('spam')"
                >
                Spam
            </button>


            <button
                @click="review('suspicious')"
                >
                Suspicious
            </button>

            <button
                class="back-button"
                @click="router.back()"
            >
                Back
            </button>
            </div>
        </div>

    </div>

</template>


<script setup>

import {ref,onMounted} from "vue";
import {useRoute, useRouter} from "vue-router";
import {api} from "@/services/api";

const router = useRouter();
const route = useRoute();
const user = ref(null);
const moderationHistory = ref([]);

const activity = ref({
    organisations:0,
    reviews:0,
    messages:0,
    saved:0
});

onMounted(async()=>{
    try{
        const data = await api.getUserDetails(route.params.id);

        user.value = data.user;
        activity.value = data.activity;
        moderationHistory.value = data.moderation_history;
    }
    catch(error){
        console.error("Failed loading user", error);
    }
});

async function review(reason) {
    try {
        await api.reviewUser(route.params.id, {
            reason: reason
        });

        const data = await api.getUserDetails(route.params.id);

        user.value = data.user;
        activity.value = data.activity;
        moderationHistory.value = data.moderation_history;
    }
    catch (error) {
        console.error(error);
    }
}

</script>

<style scoped>
.page{
    padding:40px;
    background:#F6F2ED;
    min-height:100vh;
}

.card{
    background:white;
    padding:25px;
    margin-bottom:25px;
    border-radius:15px;
    box-shadow:0 5px 15px rgba(0,0,0,.08);
}

h1{
    color:#8B5A3C;
}

h2{
    color:#8B5A3C;
    margin-bottom:20px;
}

button{
    margin-right:15px;
    padding:12px 20px;
    background:#8B5A3C;
    color:white;
    border:none;
    border-radius:8px;
    cursor:pointer;
}

.back-button{
    margin-top:20px;
    background:white;
    color:#8B5A3C;
    border:2px solid #8B5A3C;
}

hr{
    border:none;
    border-top:1px solid #eee;
    margin:15px 0;
}
</style>