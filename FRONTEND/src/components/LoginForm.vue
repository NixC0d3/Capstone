<script setup>
import { RouterLink } from "vue-router"
import { ref } from "vue"
import { loginUser } from "@/services/authService"
import { useRouter } from "vue-router"

const router = useRouter()

const email = ref("")
const password = ref("")

async function login(){
  try{
    const result = await loginUser({
      email: email.value,
      password: password.value
    });
    console.log(result);
    alert("Login successful");
  }catch(error){
    alert(error.message);
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
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
        />
        <button
          type="submit"
          class="login-btn"
        >
          Login
        </button>
      </form>

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