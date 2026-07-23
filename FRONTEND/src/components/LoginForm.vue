<script setup>
import { RouterLink, useRouter} from "vue-router";
import { ref } from "vue";
import { loginUser } from "@/services/authService";


const router = useRouter();

const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");

async function login(){
  errorMessage.value = "";
  loading.value = true;
  try{
    const result = await loginUser({
      email: email.value,
      password: password.value
    });
    // Save logged-in user
    localStorage.setItem(
      "user",
      JSON.stringify(result.user)
    );
    // Redirect based on role
    switch (result.user.role_id) {
      case 1:
        router.push("/generaluser/home");
        break;

      case 2:
        // Business dashboard
        //router.push("/business/home");
        break;

      case 3:
        // Charity dashboard
        //router.push("/charity/home");
        break;

      case 4:
        // Admin dashboard
        //router.push("/admin/dashboard");
        break;

      default:
        errorMessage.value = "Unknown user role.";
    }
  }catch(error){
    errorMessage.value =
      error.response?.data?.error ||
      error.message ||
      "Login failed.";
  }finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="login-page">

    <div class="login-card">

      <h1>CivilInfoHub</h1>

      <p class="subtitle">
        Welcome back
      </p>

      <form class="login-form"
      @submit.prevent="login"
      >

        <input
          v-model="email"
          type="text"
          placeholder="Email"
          required
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
        />
        <button
          type="submit"
          class="login-btn"
          :disabled="loading"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <p
        v-if="errorMessage"
        class="error"
      >
        {{ errorMessage }}
      </p>

      <p class="signup-text">
        Don't have an account?
        <RouterLink
          to="/signup"
          class="signup-link"
        >
          Create one
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>

.login-page{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:#F6F2ED;
}

.login-card{
    width:100%;
    max-width:420px;
    background:white;
    padding:40px;
    border-radius:18px;
    box-shadow:0 10px 30px rgba(0,0,0,.08);
}

h1{
    text-align:center;
    color:#2C2C2C;
    margin-bottom:10px;
    font-size:2.5rem;
}

.subtitle{
    text-align:center;
    color:#777;
    margin-bottom:35px;
}

.login-form{
    display:flex;
    flex-direction:column;
    gap:18px;
}

input{
    padding:14px;
    border:1px solid #D6D0C8;
    border-radius:10px;
    font-size:16px;
    outline:none;
    transition:.2s;
}

input:focus{
    border-color:#8B5A3C;
}

.login-btn{
    margin-top:10px;
    padding:14px;
    border:none;
    border-radius:10px;
    background:#8B5A3C;
    color:white;
    font-size:16px;
    cursor:pointer;
    transition:.2s;
}

.login-btn:hover{
    background:#74482D;
}

.signup-text{
    margin-top:30px;
    text-align:center;
    color:#666;
}

.signup-link{
    color:#8B5A3C;
    text-decoration:none;
    font-weight:600;
}

.signup-link:hover{
    text-decoration:underline;
}
</style>