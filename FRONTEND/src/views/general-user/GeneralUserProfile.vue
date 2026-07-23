<template>

<div class="profile-page">
    <div class="profile-header">
        <div class="avatar"> {{initials}} </div>

        <h1>{{ user.first_name }} {{ user.last_name }}</h1>

        <p> {{user.email}}</p>

    </div>

    <div class="tabs">

        <button
            :class="{ active: currentTab === 'saved' }"
            @click="currentTab = 'saved'"
        >
            Saved
        </button>

        <button @click="goInbox">
            Inbox
        </button>

        <button
            :class="{ active: currentTab === 'volunteer' }"
            @click="currentTab = 'volunteer'"
        >
            Volunteer Allocations
        </button>

        <button
            :class="{ active: currentTab === 'settings' }"
            @click="currentTab = 'settings'"
        >
            Settings
        </button>

    </div>

    <div class="content">
        <div v-if="currentTab === 'saved'">
            <h2>Saved Organisations</h2>

            <ul>
                <li
                v-for="organisation in savedOrganisations"
                :key="organisation.organisation_id"
                >
                    {{ organisation.organisation_name }}
                </li>
            </ul>
        </div>


        <div v-else-if="currentTab === 'inbox'">

            <h2>Inbox</h2>

            <div
            v-for="message in messages"
            :key="message.message_id"
            >
                <p>
                    <strong>
                        {{ message.organisation_name }}
                    </strong>
                </p>
                <p>
                    {{ message.message_text }}
                </p>
            </div>

        </div>


        <div v-else-if="currentTab === 'volunteer'">

            <h2>Volunteer Allocations</h2>

            <div
            v-for="allocation in volunteerAllocations"
            :key="allocation.id"
            >
                <p>
                    {{ allocation.organisation_name }}
                </p>
                <p>
                    {{ allocation.event_name }}
                </p>
                <p>
                    {{ allocation.date }}
                </p>
            </div>
        </div>


        <div v-else>

            <h2>Account Settings</h2>

            <button>Edit Profile</button>

            <button>Change Password</button>

        </div>

    </div>

</div>

</template>

<script setup>
import { ref, computed} from "vue";
const currentTab = ref("saved");
import { useRouter } from "vue-router";

const router = useRouter();

function goInbox() {
    router.push("/generaluser/inbox");
}

// temporary user data
// later comes from API
const user = ref({
    first_name:"John",
    last_name:"Doe",
    email:"john@email.com"
});

const savedOrganisations = ref([
    {
        organisation_id:1,
        organisation_name:"Green Earth Jamaica"
    },
    {
        organisation_id:2,
        organisation_name:"Hope Jamaica Foundation"
    }
]);

const volunteerAllocations = ref([
    {
        id:1,
        organisation_name:"Hope Jamaica Foundation",
        event_name:"Food Distribution",
        date:"12 December 2025"
    }
]);

const initials = computed(()=>{

    return (
        user.value.first_name[0] +
        user.value.last_name[0]
    ).toUpperCase();

});

</script>

<style scoped>

.profile-page{
    min-height:100vh;
    padding:40px;
    background:#F6F2ED;
}

.profile-header{
    text-align:center;
    margin-bottom:40px;
}

.avatar{
    width:90px;
    height:90px;
    margin:auto;
    border-radius:50%;
    background:#8B5A3C;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:32px;
    font-weight:bold;
}

.tabs{
    display:flex;
    justify-content:center;
    gap:40px;
    margin-bottom:30px;
    border-bottom:2px solid #ddd;
}

.tabs button{
    background:none;
    border:none;
    padding:15px 0;
    font-size:17px;
    cursor:pointer;
    color:#666;
}

.tabs button:hover{
    color:#8B5A3C;
}

.tabs button.active{
    color:#8B5A3C;
    font-weight:bold;
    border-bottom:3px solid #8B5A3C;
}

.content{
    max-width:900px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:18px;
    box-shadow:0 8px 20px rgba(0,0,0,.08);
}

ul{
    padding-left:20px;
}

li{
    margin-bottom:10px;
}

button{
    margin-right:15px;
}

</style>