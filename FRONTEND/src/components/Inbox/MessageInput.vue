<template>

<div class="input-area">
    <input
        v-model="message"
        placeholder="Write a reply..."
        @keyup.enter="submit"
    />

    <button
        @click="submit"
    >
        Send Reply
    </button>

</div>

</template>

<script setup>

import { ref } from "vue";

const emit = defineEmits(["send"]);
const message = ref("");

function submit(){
    if(!message.value.trim()) return;
    emit("send", message.value);
    message.value = "";
}

</script>

<style scoped>

.input-area{
    display:flex;
    gap:12px;
    padding:20px;
    border-top:1px solid #eee;
}

input{
    flex:1;
    padding:14px;
    border-radius:10px;
    border:1px solid #ddd;
}

button{
    padding:12px 22px;
    background:#8B5A3C;
    color:white;
    border:none;
    border-radius:10px;
    cursor:pointer;
}

</style>