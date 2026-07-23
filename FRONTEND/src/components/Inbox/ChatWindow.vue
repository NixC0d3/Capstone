<template>

<div class="chat">
    <div class="header">
        <div class="avatar">
            {{ conversation.initials }}
        </div>

        <div>
            <strong>
                {{ conversation.participant }}
            </strong>
        </div>
    </div>

    <div class="messages">
        <MessageBubble
            v-for="message in conversation.messages"
            :key="message.id"
            :message="message"
        />
    </div>
    <MessageInput
        @send="sendMessage"
    />

</div>

</template>

<script setup>

import MessageBubble from "./MessageBubble.vue";
import MessageInput from "./MessageInput.vue";

const props = defineProps({
    conversation:Object
});

function sendMessage(text){

    props.conversation.messages.push({

        id:Date.now(),
        mine:true,
        sender:"Me",
        text

    });

}

</script>

<style scoped>

.chat{
    display:flex;
    flex-direction:column;
    background:white;
    border-radius:18px;
    height:100%;
}

.header{
    display:flex;
    align-items:center;
    gap:15px;
    padding:20px;
    border-bottom:1px solid #eee;
}

.avatar{
    width:40px;
    height:40px;
    border-radius:50%;
    background:#8B5A3C;
    color:white;
    display:flex;
    justify-content:center;
    align-items:center;
}

.messages{
    flex:1;
    overflow:auto;
    padding:20px;
}

</style>