<template>
  <form class="card card-body" @submit.prevent="submitReview">
    <h5>Add a Review</h5>

    <label class="form-label">Rating</label>
    <select v-model="rating" class="form-select mb-3">
      <option v-for="value in [5,4,3,2,1]" :key="value" :value="value">
        {{ value }} star{{ value > 1 ? "s" : "" }}
      </option>
    </select>

    <label class="form-label">Review</label>
    <textarea v-model="reviewText" class="form-control mb-3" rows="3"></textarea>

    <button class="btn btn-primary">Submit Review</button>
  </form>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["submit-review"]);

const rating = ref(5);
const reviewText = ref("");

function submitReview() {
  emit("submit-review", {
    rating: rating.value,
    review_text: reviewText.value
  });

  reviewText.value = "";
  rating.value = 5;
}
</script>
