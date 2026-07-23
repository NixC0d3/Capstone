<template>

<div class="charity-card">


    <span class="category">
        {{ charity.category }}
    </span>


    <h2>
        {{ charity.name }}
    </h2>


    <div class="rating">
        ⭐ {{ charity.rating }}
    </div>


    <p class="location">
        📍 {{ charity.location }}
    </p>


    <p class="description">
        {{ charity.description }}
    </p>


    <div class="actions">

        <button class="donate">
            Donate
        </button>


        <button 
        class="learn"
        @click="learnMore"
        >
            Learn More
        </button>

    </div>


</div>

</template>


<script setup>

import { useRouter } from "vue-router";


const router = useRouter();


const props = defineProps({

    charity:{
        type:Object,
        required:true
    }

});


function learnMore(){

    router.push(`/organisation/${props.charity.id}`);

}


</script>


<style scoped>


.charity-card{

    background:white;

    width:600px;

    padding:30px;

    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    margin-bottom:25px;
}

.category{
    font-size:13px;
    color:#8B5A3C;
    text-transform:uppercase;
}

h2{
    margin:10px 0;
    color:#2C2C2C;
}

.rating{
    margin-bottom:10px;
}

.location{
    color:#666;
}


.description{
    color:#555;
    line-height:1.5;
}


.actions{
    display:flex;
    gap:15px;
    margin-top:20px;
}


button{
    padding:12px 25px;
    border-radius:10px;
    cursor:pointer;
}


.donate{
    background:#8B5A3C;
    color:white;
    border:none;
}

.learn{
    background:white;
    color:#8B5A3C;
    border:2px solid #8B5A3C;
}

@media(max-width:700px){
    .charity-card{
        width:auto;
    }
}

</style>