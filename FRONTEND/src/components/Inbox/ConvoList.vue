<template>

<div class="sidebar">

    <div
        v-for="conversation in conversations"
        :key="conversation.conversation_id"
        class="conversation"
        :class="{
            active:
            selectedConversation?.conversation_id ===
            conversation.conversation_id
        }"
        @click="$emit('select', conversation)"
    >

        <div
            class="avatar"
            :style="{ background: conversation.colour }"
        >
            {{ conversation.initials }}
        </div>

        <div class="info">

            <strong>
                {{ conversation.participant }}
            </strong>

            <p>
                {{ conversation.lastMessage }}
            </p>

        </div>

        <span>
            {{ conversation.time }}
        </span>

    </div>

</div>

</template>

<script setup>

defineProps({
    conversations:Array,
    selectedConversation:Object
});

defineEmits(["select"]);

</script>

<style scoped>

.sidebar{
    background:white;
    border-radius:18px;
    overflow:auto;
}

.conversation{
    display:flex;
    gap:15px;
    padding:18px;
    cursor:pointer;
    border-bottom:1px solid #eee;
}

.conversation:hover{
    background:#fafafa;
}

.active{
    background:#F6F2ED;
}

.avatar{
    width:42px;
    height:42px;
    border-radius:50%;
    color:white;
    display:flex;
    justify-content:center;
    align-items:center;
}

.info{
    flex:1;
}

.info p{
    margin:4px 0 0;
    color:#777;
    font-size:14px;
}

span{
    font-size:12px;
    color:#999;
}

</style>