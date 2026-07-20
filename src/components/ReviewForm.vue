<!-- Purpose: Reusable review form. It collects a rating and review text, then sends that data to the parent view. -->
<template>
  <!-- Form is prevented from refreshing the page; submitReview handles the data. -->
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
// Reusable review form. It collects a rating and review text, then sends that data to the parent view.
// emit sends the completed review back to the parent view.
// rating and reviewText are reactive variables connected to the form fields with v-model.
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
