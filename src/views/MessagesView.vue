<script setup>
import { ref } from "vue";
import MessageBox from "@/components/MessageBox.vue";

const messages = ref([]);

function sendMessage(messageText) {
  messages.value.push({
    message_id: Date.now(),
    sender_user_id: "current-user",
    message_text: messageText
  });
}
</script>

<template>
  <div class="container">
    <h1>Messages</h1>
    <MessageBox :messages="messages" @send-message="sendMessage" />
  </div>
</template>
