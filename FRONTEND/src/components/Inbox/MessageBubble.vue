<template>

<div
    class="bubble-wrapper"
    :class="{ mine: message.mine }"
>

    <div class="bubble">
        {{ message.text }}
    </div>

</div>

</template>

<script setup>

defineProps({
    message:Object
});

</script>

<style scoped>

.bubble-wrapper{
    display:flex;
    margin-bottom:18px;
}

.mine{
    justify-content:flex-end;
}

.bubble{
    max-width:65%;
    padding:15px;
    border-radius:16px;
    background:#F1ECE6;
}

.mine .bubble{
    background:#8B5A3C;
    color:white;
}

</style>