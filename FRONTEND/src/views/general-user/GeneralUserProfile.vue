<template>

<div class="profile-page">
    <div class="profile-header">
        <div class="avatar"> {{initials}} </div>
        <h1>
            {{user.display_name || `${user.first_name || ""} ${user.last_name || ""}`}}
        </h1>
        <p> {{user.email}}</p>
    </div>

    <div class="tabs">
        <button
            :class="{ active: currentTab === 'profile' }"
            @click="currentTab = 'profile'"
        >
            Profile
        </button>

        <button
            :class="{ active: currentTab === 'saved' }"
            @click="currentTab = 'saved'"
        >
            Saved
        </button>

        <button
            @click="goInbox"
        >
            Inbox
        </button>

        <button
            :class="{ active: currentTab === 'volunteer' }"
            @click="currentTab = 'volunteer'"
        >
            My Volunteer Applications
        </button>

        <button
            :class="{ active: currentTab === 'settings' }"
            @click="currentTab = 'settings'"
        >
            Settings
        </button>

    </div>

    <div class="content">
        <div v-if="currentTab === 'profile' && profile">
            <h2>My Profile</h2>

            <div class="profile-card">

                <div class="info-row">
                    <span class="label">Name</span>
                    <span>{{ profile.first_name }} {{ profile.last_name }}</span>
                </div>

                <div class="info-row">
                    <span class="label">Email</span>
                    <span>{{ profile.email }}</span>
                </div>

                <div class="info-row">

                    <div class="section-header">
                        <span class="label">Interests</span>

                        <button
                            class="edit-btn"
                            @click="openInterestEditor"
                        >
                            + Edit
                        </button>
                    </div>
                    <div class="tags">
                        <span
                            v-for="interest in profile.preferences"
                            :key="interest.category_id"
                            class="tag"
                        >
                            {{ interest.category_name }}
                        </span>
                        <span
                            v-if="!profile.preferences.length"
                            class="empty"
                        >
                            No interests selected
                        </span>

                    </div>

                    <div
                        v-if="showInterestEditor"
                        class="editor"
                    >
                        <h3>Select Interests</h3>

                        <label
                            v-for="interest in interests"
                            :key="interest.category_id"
                        >

                            <input
                                type="checkbox"
                                :value="interest.category_id"
                                v-model="selectedInterests"
                            >

                            {{ interest.category_name }}

                        </label>

                        <button @click="saveInterests">
                            Save Interests
                        </button>
                    </div>
                </div>

                <div class="info-row">
                    <div class="section-header">
                        <span class="label">Skills</span>

                        <button
                            class="edit-btn"
                            @click="openSkillEditor"
                        >
                            + Edit
                        </button>
                    </div>
                             
                    <div class="tags">
                        <span
                            v-for="skill in profile.skills"
                            :key="skill"
                            class="skill-tag"
                        >
                            {{ skill }}
                        </span>

                        <span
                            v-if="!profile.skills.length"
                            class="empty"
                        >
                            No skills added
                        </span>
                    </div>

                    <div
                        v-if="showSkillEditor"
                        class="editor"
                    >
                        <h3>Select Skills</h3>

                        <label
                            v-for="skill in skills"
                            :key="skill"
                        >
                            <input
                                type="checkbox"
                                :value="skill"
                                v-model="selectedSkills"
                            >
                            {{skill}}
                        </label>
                        <button @click="saveSkills">
                            Save Skills
                       </button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else-if="currentTab === 'profile'">
            Loading profile...
        </div>

        <div v-else-if="currentTab === 'saved'">
            <h2>Saved Organisations</h2>
            <div v-if="savedOrganisations.length">
                <ul>
                    <li
                        v-for="organisation in savedOrganisations"
                        :key="organisation.organisation_id"
                        @click="openOrganisation(organisation.organisation_id)"
                    >
                        {{ organisation.organisation_name }}
                    </li>
                </ul>
            </div>
            <p v-else>
                You have no saved organisations yet.
            </p>
        </div>


        <div v-else-if="currentTab === 'inbox'">
            <h2>Inbox</h2>
            <div
                v-if="messages.length"
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
            <p v-else>
                No messages yet.
            </p>
        </div>


        <div v-else-if="currentTab === 'volunteer'">
            <MyVolunteerApplications />
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
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { api } from "@/services/api";
import MyVolunteerApplications from "@/components/MyVolunteerApplications.vue";

const router = useRouter();
const currentTab = ref("profile");
const user = ref({});
const savedOrganisations = ref([]);
const messages = ref([]);
const volunteerAllocations = ref([]);
const profile = ref(null);

const showSkillEditor = ref(false);
const showInterestEditor = ref(false);

const skills = ref([]);
const interests = ref([]);

const selectedSkills = ref([]);
const selectedInterests = ref([]);


const initials = computed(() => {
    const name =
        user.value.display_name ||
        `${user.value.first_name || ""} ${user.value.last_name || ""}`.trim();

    return name
        .split(" ")
        .filter(Boolean)
        .map(word => word.charAt(0))
        .join("")
        .substring(0, 2)
        .toUpperCase();
});

async function loadProfile(){
    const storedUser = JSON.parse(localStorage.getItem("user"));

    if(!storedUser){
        return;
    }
    user.value = storedUser;
    try{
        savedOrganisations.value = await api.getSavedOrganisations(storedUser.user_id);
        profile.value = await api.getProfile(storedUser.user_id);
    }catch(error){
        console.error("Error loading saved organisations:", error);
    }
}

function openOrganisation(id){
    router.push(`/organisation/${id}`);
}

function goInbox(){
    const user = JSON.parse(localStorage.getItem("user"));

    if(!user){
        router.push("/login");
        return;
    }
    if(user.role === "charity"){
        router.push("/charity-user/inbox");
    }
    else if(user.role === "business"){
        router.push("/business-user/inbox");
    }
    else{
        router.push("/generaluser/inbox");
    }
}

onMounted(() => {
    loadProfile();
});

async function openSkillEditor(){
    skills.value = await api.getSkills();
    selectedSkills.value = [
        ...profile.value.skills
    ];
    showSkillEditor.value = true;
}

async function saveSkills(){
    await api.updateSkills(
        user.value.user_id,
        selectedSkills.value
    );
    profile.value.skills = [
        ...selectedSkills.value
    ];
    showSkillEditor.value = false;
}

async function openInterestEditor(){
    interests.value = await api.getInterests();
    console.log(
        "AVAILABLE INTERESTS:",
        interests.value
    );
    selectedInterests.value = profile.value.preferences.map(
        interest => interest.category_id
    );
    console.log(
        "SELECTED:",
        selectedInterests.value
    );
    showInterestEditor.value = true;
}

async function saveInterests(){
    await api.updateInterests(
        user.value.user_id,
        selectedInterests.value
    );
    profile.value = await api.getProfile(
        user.value.user_id
    );
    showInterestEditor.value = false;
}
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
    width:110px;
    height:110px;
    border-radius:50%;
    background:linear-gradient(135deg,#8B5A3C,#B8865B);
    color:white;
    font-size:38px;
    font-weight:bold;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:auto;
    box-shadow:0 10px 25px rgba(139,90,60,.35);
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
    list-style:none;
    padding:18px;
    margin-bottom:15px;
    border-radius:14px;
    background:white;
    border:1px solid #E7DDD2;
    box-shadow:0 4px 12px rgba(0,0,0,.05);
    transition:.25s;
}

li:hover{
    transform:translateY(-3px);
    border-color:#8B5A3C;
    box-shadow:0 8px 18px rgba(0,0,0,.12);
}
button{
    margin-right:15px;
}
.profile-card{
    margin-top:20px;
    background:#FAF8F5;
    border-radius:16px;
    padding:25px;
    border:1px solid #E7DDD2;
}

.info-row{
    margin-bottom:25px;
}

.label{
    display:block;
    font-weight:700;
    color:#8B5A3C;
    margin-bottom:10px;
}

.tags{
    display:flex;
    flex-wrap:wrap;
    gap:10px;
}

.tag{
    background:#EFE5DB;
    color:#8B5A3C;
    padding:8px 16px;
    border-radius:999px;
    font-size:14px;
    font-weight:600;
}

.skill-tag{
    background:#8B5A3C;
    color:white;
    padding:8px 16px;
    border-radius:999px;
    font-size:14px;
}

.empty{
    color:#888;
    font-style:italic;
}
.section-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.edit-btn{
    background:#8B5A3C;
    color:white;
    border:none;
    padding:6px 14px;
    border-radius:8px;
    cursor:pointer;
}

.editor{
    margin-top:20px;
    padding:20px;
    background:#FAF8F5;
    border-radius:12px;
    border:1px solid #E7DDD2;

    display:flex;
    flex-direction:column;
    gap:10px;
}

.editor label{
    display:flex;
    gap:10px;
}

.editor button{
    margin-top:15px;
    background:#8B5A3C;
    color:white;
    border:none;
    padding:10px;
    border-radius:8px;
}
</style>
