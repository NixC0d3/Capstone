<template>
  <div class="signup-container">
  <h1>CivilInfoHub</h1>


    <div class="progress">
    Step {{step}} / {{totalSteps}}
    </div>

      <!-- STEP 1 PERSONAL INFO -->
      <div v-if="step === 1">
      <h2>Create your profile</h2>


      <input 
      v-model="user.first_name"
      placeholder="First Name"
      />

      <input 
      v-model="user.last_name"
      placeholder="Last Name"
      />

      <input 
      v-model="user.email"
      type="email"
      placeholder="Email"
      />

      <input
      v-model="user.password"
      type="password"
      placeholder="Password"
      />


      <select v-model="user.location">
        <option disabled value="">Location</option>
        <option 
          v-for="parish in parishes"
          :key="parish"
          :value="parish"
        >
          {{ parish }}
        </option>
      </select>


      <h3>What describes you?</h3>
      <button
      v-for="type in userTypes"
      :key="type"
      @click="user.userType = type"
      :class="{selected:user.userType === type}"
      >

      {{type}}

      </button>
    </div>


    <!-- STEP 2 BUSINESS INTERESTS -->
    <div v-if="step === 2">
      <h2>Businesses you want to discover</h2>

      <div class="grid">
        <button
          v-for="item in businessInterests"
          :key="item.id"
          @click="toggleBusiness(item)"
          :class="{
          selected:user.businessInterests.some(i => i.id === item.id)
          }"
          >

          {{item.name}}
        </button>
      </div>
    </div>


    <!-- STEP 3 CHARITIES -->
    <div v-if="step === 3">
      <h2>Causes you care about</h2>
      <div class="grid">

        <button
        v-for="item in charityInterests"
        :key="item"
        @click="toggleCharity(item)"
        :class="{
        selected:user.charityInterests.some(i => i.id === item.id)
        }"
        >

        {{item.name}}

        </button>
      </div>
    </div>

    <div v-if="step === 4">
      <h2>What skills would you like to contribute?</h2>

      <p>
        These help charities find volunteers with the right experience.
      </p>

      <div class="grid">
          <button
          v-for="skill in skills"
          :key="skill"
          @click="toggleSkill(skill)"
          :class="{ selected: user.skills.includes(skill) }"
          >
          {{ skill }}
        </button>

      </div>
    </div>

    <!-- STEP 5 REVIEW -->
    <div v-if="step === 5">
      <h2>Your Profile</h2>
      <pre>{{user}}</pre>
      </div>
      
      <div class="buttons">
        <button v-if="step > 1"
          @click="step--"
          >
          Back
        </button>

        <button v-if="step < totalSteps"
          @click="next"
          >
          Continue
        </button>

        <button v-if="step === totalSteps"
          @click="finish"
          >
          Create Account
        </button>
      </div>
    </div>

</template>

<script setup>

import { reactive, ref } from "vue"
import { api } from "@/services/api"

const step = ref(1)
const totalSteps = 5

const user = reactive({
  first_name:"",
  last_name:"",
  email:"",
  password:"",

  location:"",

  userType:"",

  businessInterests:[],
  charityInterests:[],
  skills:[]
})


const userTypes = [
  "Community Member",
  "Business Owner",
  "Charity Representative"
]

const businessInterests = [
  {id:1, name:"Food / Restaurants"},
  {id:2, name:"Retail / Clothing"},
  {id:3, name:"Health & Wellness"},
  {id:4, name:"Beauty & Personal Care"},
  {id:5, name:"Arts & Crafts"},
  {id:6, name:"Home & Garden"},
  {id:7, name:"Professional Services"},
  {id:8, name:"Technology Services"},
  {id:9, name:"Automotive"},
  {id:10, name:"Construction"},
  {id:11, name:"Entertainment"},
  {id:12, name:"Agriculture"},
  {id:13, name:"Marketing & Design"}
]


const charityInterests = [
  {id:14, name:"Education & Youth Development"},
  {id:15, name:"Poverty Alleviation"},
  {id:16, name:"Food Security"},
  {id:17, name:"Environmental Conservation"},
  {id:18, name:"Animal Welfare"},
  {id:19, name:"Community Development"},
  {id:20, name:"Arts & Culture"},
  {id:21, name:"Disaster Relief"},
  {id:22, name:"Elderly Care"},
  {id:23, name:"Homeless Support"},
  {id:24, name:"Faith-Based Initiatives"}
]

const skills = [
  "Teaching",
  "Mentoring",
  "Graphic Design",
  "Programming",
  "Photography",
  "Accounting",
  "Legal Services",
  "Construction",
  "First Aid",
  "Marketing",
  "Event Planning",
  "Cooking",
  "Driving",
  "Administration",
  "Other"
]

const parishes = [
  "Kingston",
  "St. Andrew",
  "St. Thomas",
  "Portland",
  "St. Mary",
  "St. Ann",
  "Trelawny",
  "St. James",
  "Hanover",
  "Westmoreland",
  "St. Elizabeth",
  "Manchester",
  "Clarendon",
  "St. Catherine"
]


function toggleBusiness(item){
  const exists = user.businessInterests.some(
    i => i.id === item.id
  )

  if(exists){
    user.businessInterests =
    user.businessInterests.filter(
      i => i.id !== item.id
    )
  }else{
    user.businessInterests.push(item)
  }
}

function toggleCharity(item){
  const exists = user.charityInterests.some(
    i => i.id === item.id
  )
  if(exists){
    user.charityInterests =
    user.charityInterests.filter(
      i => i.id !== item.id
    )
  }else{
      user.charityInterests.push(item)
  }
}

function toggleSkill(skill) {
  if (user.skills.includes(skill)) {
    user.skills = user.skills.filter(s => s !== skill)
  } else {
    user.skills.push(skill)
  }
}

function next() {
  // Businesses and charities skip onboarding
  if (step.value === 1 && user.userType !== "Community Member"
  ){
    finish()
    return
  }if (step.value < totalSteps) {
    step.value++
  }
}

async function finish(){
  try{
    const preferences = [
      ...user.businessInterests.map(
        item => item.id
      ),
      ...user.charityInterests.map(
        item => item.id
      )
    ]
  
  let role_id = 1

  if(user.userType === "Business Owner"){
    role_id = 2
  }
  if(user.userType === "Charity Representative"){
    role_id = 3
  }

  const response = await api.registerUser({
    first_name:user.first_name,
    last_name:user.last_name,
    email:user.email,
    password:user.password,
    role_id:role_id,

    preferences:preferences,
    skills:user.skills
  })
  console.log(response)

  alert("Account created successfully")
  }catch(error){

    console.error(error)
    alert(error.message)
  }
}

</script>

<style scoped>
.signup-container{
  max-width:500px;
  margin:40px auto;
  padding:40px;
  background:white;
  border-radius:18px;
  box-shadow:0 10px 30px rgba(0,0,0,.08);
  font-family:sans-serif;
}

.progress{
  text-align:center;
  color:#777;
  margin-bottom:25px;
  font-size:14px;
}

h1{
  text-align:center;
  color:#2C2C2C;
  margin-bottom:10px;
  font-size:2.5rem;
}

h2{
  text-align:center;
  color:#2C2C2C;
  margin-bottom:25px;
  font-size:2rem;
}

h3{
  color:#2C2C2C;
  margin-top:25px;
  font-size:1.1rem;
}

p{
  color:#666;
  line-height:1.5;
}

/* Inputs */
input, select{
  display:block;
  width:100%;
  padding:14px;
  margin:12px 0;
  border:1px solid #D6D0C8;
  border-radius:10px;
  font-size:16px;
  outline:none;
  background:white;
  transition:.2s;
}

input:focus,
select:focus{
  border-color:#8B5A3C;
  box-shadow:0 0 0 3px rgba(139,90,60,.15);
}

/* Option buttons */
.grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:12px;
}

button{
  padding:12px;
  border-radius:10px;
  border:1px solid #D6D0C8;
  background:white;
  color:#2C2C2C;
  cursor:pointer;
  font-size:14px;
  transition:.2s;
}

button:hover{
  border-color:#8B5A3C;
}

/* Selected options */
button.selected{
  background:#8B5A3C;
  border-color:#8B5A3C;
  color:white;
}

/* Navigation */
.buttons{
  margin-top:35px;
  display:flex;
  justify-content:space-between;
  gap:15px;
}

.buttons button{
  flex:1;
  background:#8B5A3C;
  color:white;
  border:none;
  font-size:16px;
  padding:14px;
}
.buttons button:hover{
  background:#74482D;
}

/* Review box */
pre{
  background:#F6F2ED;
  padding:20px;
  border-radius:10px;
  color:#2C2C2C;  
  overflow:auto;
  font-size:14px;
}



/* Mobile */
@media(max-width:600px){
  .signup-container{
  margin:20px;
  padding:25px;
  }
  .grid{
    grid-template-columns:1fr;
  }
}

</style>