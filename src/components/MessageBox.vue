<template>
  <section class="card">
    <div class="card-header">Messages</div>

    <div class="card-body">
      <div v-if="messages.length === 0" class="text-muted">No messages yet.</div>

      <div v-for="message in messages" :key="message.message_id" class="border rounded p-2 mb-2">
        <small class="text-muted">Sender #{{ message.sender_user_id }}</small>
        <p class="mb-0">{{ message.message_text }}</p>
      </div>
    </div>

    <div class="card-footer">
      <form class="d-flex gap-2" @submit.prevent="send">
        <input v-model="messageText" class="form-control" placeholder="Type a message" />
        <button class="btn btn-primary">Send</button>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";

defineProps({
  messages: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(["send-message"]);
const messageText = ref("");

function send() {
  if (!messageText.value.trim()) return;

  emit("send-message", messageText.value);
  messageText.value = "";
}
</script>
