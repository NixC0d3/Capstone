<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import ReviewForm from "@/components/ReviewForm.vue";
import ReviewList from "@/components/ReviewList.vue";
import MessageBox from "@/components/MessageBox.vue";
import { api } from "@/services/api";

const route = useRoute();
const organisation = ref({});
const reviews = ref([]);
const messages = ref([]);

onMounted(async () => {
  try {
    organisation.value = await api.getOrganisation(route.params.id);
  } catch (error) {
    console.error(error);
  }
});

function handleReview(review) {
  console.log("Submit review:", review);
}

function handleMessage(messageText) {
  messages.value.push({
    message_id: Date.now(),
    sender_user_id: "current-user",
    message_text: messageText
  });
}
</script>

<template>
  <div class="container">
    <h1>{{ organisation.organisation_name || "Organisation Details" }}</h1>
    <p class="text-muted">{{ organisation.organisation_type }}</p>
    <p>{{ organisation.description }}</p>

    <div class="row g-4">
      <div class="col-md-6">
        <ReviewForm @submit-review="handleReview" />
      </div>

      <div class="col-md-6">
        <MessageBox :messages="messages" @send-message="handleMessage" />
      </div>

      <div class="col-12">
        <ReviewList :reviews="reviews" />
      </div>
    </div>
  </div>
</template>
