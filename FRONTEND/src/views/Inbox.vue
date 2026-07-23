<template>
  <div class="inbox-page">

    <ConversationList
      :conversations="conversations"
      :selectedConversation="selectedConversation"
      @select="selectConversation"
    />

    <ChatWindow
      v-if="selectedConversation"
      :conversation="selectedConversation"
    />

    <div
      v-else
      class="empty"
    >
      Select a conversation
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import ConversationList from "@/components/Inbox/ConvoList.vue";
import ChatWindow from "@/components/Inbox/ChatWindow.vue";

import { useRoute } from "vue-router";

const route = useRoute();
const organisationId = route.query.organisation;

const conversations = ref([
  {
    conversation_id:1,
    organisation_id:1,
    participant:"John Brown",
    lastMessage:"I'm interested in your services.",
    time:"12:03 PM",
    initials:"J",
    colour:"#8B5A3C",
    messages:[
        {
            id:1,
            sender:"John Brown",
            mine:false,
            text:"Hi, I'm interested in your services."
        },
        {
            id:2,
            sender:"Me",
            mine:true,
            text:"Thanks for reaching out! We'd be happy to help."
        }
    ]
},
{
    conversation_id:2,
    organisation_id:2,
    participant:"Sarah Williams",
    lastMessage:"Thank you for your response.",
    time:"Yesterday",
    initials:"S",
    colour:"#7B3FA0",
    messages:[]
}
]);

const selectedConversation = ref(null);
function selectConversation(conversation) {
    selectedConversation.value = conversation;
}

onMounted(() => {
    if (organisationId) {
        const conversation = conversations.value.find(
            c => c.organisation_id == organisationId
        );

        if (conversation) {
            selectedConversation.value = conversation;
        }
    }else if (conversations.value.length) {
      selectedConversation.value = conversations.value[0];
    }
});
</script>

<style scoped>

.inbox-page{
    display:grid;
    grid-template-columns:340px 1fr;
    gap:25px;
    height:80vh;
}

.empty{
    display:flex;
    align-items:center;
    justify-content:center;
    background:white;
    border-radius:18px;
}

</style>