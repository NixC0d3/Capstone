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
        Loading conversations...
      </div>

      <div
        v-else-if="conversations.length === 0"
        class="empty-list"
      >
        No conversations yet.
      </div>

      <div
        v-else
        v-for="conversation in conversations"
        :key="conversation.conversation_id"
        class="conversation-card"
        :class="{
          active:
            selectedConversation &&
            selectedConversation.conversation_id === conversation.conversation_id
        }"
        @click="selectConversation(conversation)"
      >
        <div class="avatar">
          {{ conversation.initials }}
        </div>

        <div>
          <h3>{{ conversation.participant }}</h3>
          <p>{{ conversation.lastMessage }}</p>
          <small>{{ conversation.time }}</small>
        </div>
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
          placeholder="Write a message..."
          @keyup.enter="sendReply"
        />

        <button @click="sendReply">
          Send
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
const conversations = ref([]);
const selectedConversation = ref(null);
const newMessage = ref("");
const loading = ref(true);


function getCurrentUserId() {
  return currentUser.value?.user_id || currentUser.value?.id;
}


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


function isOrganisationOwner() {
  const roleId = Number(currentUser.value?.role_id);

  // 2 = Business Owner
  // 3 = Charity Owner
  return roleId === 2 || roleId === 3;
}


function formatConversationListItem(row) {
  const participant = isOrganisationOwner()
    ? row.general_user_name
    : row.organisation_name;

  return {
    conversation_id: row.conversation_id,
    organisation_id: row.organisation_id,
    general_user_id: row.general_user_id,
    participant: participant,
    initials: getInitials(participant),
    lastMessage: row.last_message || "No messages yet",
    time: formatTime(row.last_message_time || row.last_message_at || row.created_at)
  };
}

function buildSelectedConversation(data) {
  const userId = getCurrentUserId();

  const conversationInfo = data.conversation || {};
  const organisationInfo = data.organisation || {};

  const conversationId =
    data.conversation_id ||
    conversationInfo.conversation_id ||
    null;

  const organisationId =
    organisationInfo.organisation_id ||
    conversationInfo.organisation_id ||
    null;

  const participant = isOrganisationOwner()
  ? conversationInfo.general_user_name
  : conversationInfo.organisation_name ||
    organisationInfo.organisation_name ||
    "Conversation";

  const messages = (data.messages || []).map(message => {
    return {
      id: message.message_id,
      conversation_id: message.conversation_id,
      sender_user_id: message.sender_user_id,
      sender: message.sender_name,
      mine: message.sender_user_id === userId,
      text: message.message_text,
      sent_at: message.sent_at
    };
  });

  selectedConversation.value = {
    conversation_id: conversationId,
    organisation_id: organisationId,
    participant: participant,
    initials: getInitials(participant),
    lastMessage: messages.length
      ? messages[messages.length - 1].text
      : "No messages yet",
    time: messages.length
      ? formatTime(messages[messages.length - 1].sent_at)
      : "",
    messages: messages
  };
}


async function loadInbox() {
  const userId = getCurrentUserId();

  const data = await api.getInbox(userId);

  conversations.value = data.map(row => formatConversationListItem(row));
}


async function loadConversationByOrganisation(organisationId) {
  const userId = getCurrentUserId();

  const data = await api.getConversation(userId, organisationId);

  buildSelectedConversation(data);
}


async function selectConversation(conversation) {
  try {
    const userId = getCurrentUserId();

    const data = await api.getConversationById(
      conversation.conversation_id,
      userId
    );

    buildSelectedConversation(data);

  } catch (error) {
    console.error("Error loading selected conversation:", error);
    alert("Could not load this conversation.");
  }
}


async function sendReply() {
  try {
    const messageText = newMessage.value.trim();

    if (!messageText) {
      return;
    }

    if (!selectedConversation.value) {
      alert("No conversation selected.");
      return;
    }

    const payload = {
      sender_user_id: getCurrentUserId(),
      message_text: messageText
    };

    if (selectedConversation.value.conversation_id) {
      payload.conversation_id = selectedConversation.value.conversation_id;
    } else {
      payload.organisation_id = selectedConversation.value.organisation_id;
    }

    const response = await api.sendMessage(payload);

    newMessage.value = "";

    await loadInbox();

    if (response.conversation_id) {
      await selectConversation({
        conversation_id: response.conversation_id
      });
    }

  } catch (error) {
    console.error("Error sending message:", error);
    alert("Message failed. Check browser console and backend terminal.");
  }
}


async function loadPage() {
  try {
    loading.value = true;

    currentUser.value = JSON.parse(localStorage.getItem("user") || "{}");

    if (!getCurrentUserId()) {
      alert("You must be logged in to view messages.");
      return;
    }

    await loadInbox();

    const organisationId = route.query.organisation;

    if (organisationId) {
      await loadConversationByOrganisation(organisationId);
      return;
    }

    if (conversations.value.length > 0) {
      await selectConversation(conversations.value[0]);
    }

  } catch (error) {
    console.error("Error loading inbox:", error);
    alert("Could not load inbox. Check browser console and backend terminal.");
  } finally {
    loading.value = false;
  }
}


onMounted(async () => {
  await loadPage();
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
