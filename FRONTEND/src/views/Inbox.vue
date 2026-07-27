<template>

  <button 
      class="back-btn"
      @click="$router.back()"
  >
      ← Back
  </button>

  <div class="inbox-page">

    <!-- LEFT SIDE: Conversation List -->
    <div class="conversation-list">
      <div v-if="loading" class="empty-list">
        Loading conversation...
      </div>

      <div
        v-else-if="selectedConversation"
        class="conversation-card active"
      >
        <div class="avatar">
          {{ selectedConversation.initials }}
        </div>

        <div>
          <h3>{{ selectedConversation.participant }}</h3>
          <p>{{ selectedConversation.lastMessage }}</p>
          <small>{{ selectedConversation.time }}</small>
        </div>
      </div>

      <div v-else class="empty-list">
        No conversation selected.
      </div>
    </div>


    <!-- RIGHT SIDE: Chat Window -->
    <div v-if="selectedConversation" class="chat-window">

      <div class="chat-header">
        <div class="avatar">
          {{ selectedConversation.initials }}
        </div>

        <h2>{{ selectedConversation.participant }}</h2>
      </div>

      <div class="messages-area">
        <div
          v-if="selectedConversation.messages.length === 0"
          class="no-messages"
        >
          No messages yet. Start the conversation below.
        </div>

        <div
          v-for="message in selectedConversation.messages"
          :key="message.id"
          :class="message.mine ? 'message-row mine' : 'message-row theirs'"
        >
          <div class="message-bubble">
            {{ message.text }}
          </div>
        </div>
      </div>

      <div class="reply-box">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Write a reply..."
          @keyup.enter="sendReply"
        />

        <button @click="sendReply">
          Send Reply
        </button>
      </div>

    </div>

    <div v-else class="empty">
      Select a conversation
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { api } from "@/services/api";

const route = useRoute();

const currentUser = ref(null);
const organisation = ref(null);
const selectedConversation = ref(null);
const newMessage = ref("");
const loading = ref(true);


function getInitials(name) {
  if (!name) {
    return "?";
  }

  return name
    .split(" ")
    .filter(Boolean)
    .map(word => word[0])
    .join("")
    .substring(0, 2)
    .toUpperCase();
}


function formatTime(dateValue) {
  if (!dateValue) {
    return "";
  }

  const date = new Date(dateValue);

  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  });
}


function buildConversation(data) {
  const org = data.organisation;
  const messageRows = data.messages || [];

  const formattedMessages = messageRows.map(message => {
    return {
      id: message.message_id,
      sender_user_id: message.sender_user_id,
      sender: message.sender_name,
      mine: message.sender_user_id === currentUser.value.user_id,
      text: message.message_text,
      sent_at: message.sent_at
    };
  });

  const lastMessage = formattedMessages.length
    ? formattedMessages[formattedMessages.length - 1]
    : null;

  selectedConversation.value = {
    conversation_id: formattedMessages.length
      ? formattedMessages[0].conversation_id
      : null,

    organisation_id: org.organisation_id,
    participant: org.organisation_name,
    initials: getInitials(org.organisation_name),
    lastMessage: lastMessage ? lastMessage.text : "Start a conversation",
    time: lastMessage ? formatTime(lastMessage.sent_at) : "",
    messages: formattedMessages
  };
}


async function loadConversation() {
  try {
    loading.value = true;

    currentUser.value = JSON.parse(localStorage.getItem("user"));

    if (!currentUser.value || !currentUser.value.user_id) {
      alert("You must be logged in to view messages.");
      return;
    }

    const organisationId = route.query.organisation;

    if (!organisationId) {
      console.log("No organisation selected in URL.");
      return;
    }

    const data = await api.getConversation(
      currentUser.value.user_id,
      organisationId
    );

    organisation.value = data.organisation;

    buildConversation(data);

    console.log("Conversation loaded:", data);

  } catch (error) {
    console.error("Error loading conversation:", error);
    alert("Could not load conversation. Check browser console and backend terminal.");
  } finally {
    loading.value = false;
  }
}


async function sendReply() {
  try {
    if (!newMessage.value.trim()) {
      return;
    }

    if (!currentUser.value || !organisation.value) {
      alert("Conversation is not ready yet.");
      return;
    }

    await api.sendMessage({
      user_id: currentUser.value.user_id,
      organisation_id: organisation.value.organisation_id,
      message_text: newMessage.value
    });

    newMessage.value = "";

    await loadConversation();

  } catch (error) {
    console.error("Error sending message:", error);
    alert("Message failed. Check browser console and backend terminal.");
  }
}


onMounted(async () => {
  await loadConversation();
});
</script>


<style scoped>
.inbox-page {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 25px;
  height: 80vh;
}
.back-btn{
    background:none;
    border:none;
    color:#8B5A3C;
    cursor:pointer;
    font-size:16px;
    margin-bottom:25px;
}

.back-btn:hover{
    text-decoration:underline;
}

.conversation-list {
  background: #f6f2ed;
  border-radius: 0 18px 18px 0;
  overflow-y: auto;
}

.conversation-card {
  display: flex;
  gap: 15px;
  padding: 18px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}

.conversation-card.active {
  background: #eee8df;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #8b5a3c;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.conversation-card h3 {
  margin: 0;
  font-size: 16px;
}

.conversation-card p {
  margin: 4px 0;
  color: #777;
}

.conversation-card small {
  color: #999;
}

.chat-window {
  background: white;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.chat-header h2 {
  margin: 0;
  font-size: 20px;
}

.messages-area {
  flex: 1;
  padding: 25px;
  overflow-y: auto;
}

.no-messages {
  color: #777;
  text-align: center;
  margin-top: 50px;
}

.message-row {
  display: flex;
  margin-bottom: 15px;
}

.message-row.mine {
  justify-content: flex-end;
}

.message-row.theirs {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 55%;
  padding: 14px 18px;
  border-radius: 14px;
  background: #f1ede7;
}

.message-row.mine .message-bubble {
  background: #8b5a3c;
  color: white;
}

.reply-box {
  display: flex;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.reply-box input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.reply-box button {
  background: #8b5a3c;
  color: white;
  border: none;
  padding: 12px 22px;
  border-radius: 8px;
  cursor: pointer;
}

.empty,
.empty-list {
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 18px;
  color: #777;
  padding: 20px;
}
</style>
