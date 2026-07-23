<template>

<div class="profile-page">

    <div class="profile-header">

        <div class="avatar">P</div>

        <h1>John Doe</h1>

        <p>john@email.com</p>

    </div>

    <div class="tabs">

        <button
            :class="{ active: currentTab === 'saved' }"
            @click="currentTab = 'saved'"
        >
            Saved
        </button>

        <button
            :class="{ active: currentTab === 'inbox' }"
            @click="currentTab = 'inbox'"
        >
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
                <li>Island Coffee House</li>
                <li>Hope Jamaica Foundation</li>
                <li>Green Earth Jamaica</li>
            </ul>

        </div>


        <div v-else-if="currentTab === 'inbox'">

            <h2>Inbox</h2>

            <p>Green Earth: Thank you for your support!</p>

            <p>Hope Jamaica: Volunteer event this Saturday.</p>

        </div>


        <div v-else-if="currentTab === 'volunteer'">

            <h2>Volunteer Allocations</h2>

            <p>Hope Jamaica Foundation</p>

            <p>Food Distribution</p>

            <p>12 December 2025</p>

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
import { ref } from "vue";

const currentTab = ref("saved");
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