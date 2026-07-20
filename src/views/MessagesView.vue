<!-- Purpose: Page-level messages screen using the reusable MessageBox component. -->
<script setup>
// Page-level messages screen using the reusable MessageBox component.
// messages stores the current messages shown on this page.
// sendMessage adds a demo message to the screen when MessageBox emits send-message.
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
  <!-- Page-level messages screen using the reusable MessageBox component. -->
  <div class="container">
    <h1>Messages</h1>
    <MessageBox :messages="messages" @send-message="sendMessage" />
  </div>
</template>
