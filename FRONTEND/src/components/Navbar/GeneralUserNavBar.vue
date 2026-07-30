<template>

<nav class="navbar">
    <router-link class="brand" to="/generaluser/home">
      <img
        src="/CIH_logo.jpeg"
        alt="CivilInfoHub Logo"
        class="brand-logo"
      />
      <span>CivilInfoHub</span>
    </router-link>

    <div class="nav-links">
        <router-link to="/generaluser/home">
            Home
        </router-link>

        <router-link to="/generaluser/charities">
            Charities
        </router-link>
        
        <router-link to="/generaluser/volunteer-opportunities">
            Volunteer Opportunities
        </router-link>

        <router-link to="/about">
            About
        </router-link>

    </div>

    <div class="user-actions">

        <button class="profile-button" @click="goProfile">
            {{ initials }}
        </button>

        <button class="logout-button" @click="logout">
            Logout
        </button>
    </div>

</nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { computed } from "vue";
const router = useRouter();

const user = JSON.parse(
    localStorage.getItem("user")
);

const initials = computed(() => {
    if (!user) {
        return "U";
    }

    const name =
        user.display_name ||
        `${user.first_name || ""} ${user.last_name || ""}`.trim();

    return name
        .split(" ")
        .filter(Boolean)
        .map(word => word.charAt(0))
        .join("")
        .substring(0, 2)
        .toUpperCase();
});


function goProfile(){
    router.push("/generaluser/profile");
}

function logout(){
    // later this will clear authentication
    localStorage.removeItem("user");
    router.push("/login");
}
</script>


<style scoped>

.navbar {
    height:70px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 40px;
    background:white;
    box-shadow:0 3px 15px rgba(0,0,0,.08);
}

.brand {
    display:flex;
    align-items:center;
    gap:10px;
    text-decoration:none;
    font-size:24px;
    font-weight:bold;
    color:#8B5A3C;
}

.brand-logo {
    width:38px;
    height:38px;
    object-fit:contain;
    border-radius:50%;
}

.nav-links {
    display:flex;
    gap:35px;
}

.nav-links a {
    text-decoration:none;
    color:#444;
    font-size:16px;
}

.nav-links a.router-link-active {
    color:#8B5A3C;
    font-weight:bold;
}

.user-actions {
    display:flex;
    align-items:center;
    gap:15px;
}

.profile-button {
    width:40px;
    height:40px;
    border-radius:50%;
    border:none;
    background:#8B5A3C;
    color:white;
    cursor:pointer;
    font-weight:bold;
}


.logout-button {
    background:transparent;
    border:2px solid #8B5A3C;
    color:#8B5A3C;
    padding:10px 18px;
    border-radius:10px;
    cursor:pointer;
}

.logout-button:hover {
    background:#8B5A3C;
    color:white;
}


</style>
