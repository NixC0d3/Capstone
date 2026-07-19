<template>
  <section>
    <h5>Reviews</h5>

    <div v-if="reviews.length === 0" class="alert alert-light">
      No reviews yet.
    </div>

    <div v-for="review in reviews" :key="review.review_id" class="border rounded p-3 mb-2">
      <strong>{{ review.rating }}/5</strong>
      <p class="mb-0">{{ review.review_text }}</p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  reviews: {
    type: Array,
    default: () => []
  }
});
</script>
