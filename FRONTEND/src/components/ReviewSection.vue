
<template>

<section class="reviews-section">
  <div class="reviews-header">

    <h2>
      Reviews
    </h2>

    <button
      class="add-review-btn"
      @click="showForm = !showForm"
    >
      {{ showForm ? "−" : "+" }}
    </button>
  </div>

  <div
    v-if="showForm"
    class="review-form"
  >
    <select v-model="newReview.rating">
      <option :value="5">⭐⭐⭐⭐⭐</option>
      <option :value="4">⭐⭐⭐⭐</option>
      <option :value="3">⭐⭐⭐</option>
      <option :value="2">⭐⭐</option>
      <option :value="1">⭐</option>
    </select>

    <textarea
      v-model="newReview.review_text"
      placeholder="Write your review..."
    ></textarea>

    <button
      class="submit-btn"
      @click="submitReview"
    >
      Submit Review
    </button>
  </div>

  <!-- Existing Reviews -->
  <div
    v-if="reviews.length"
  >
    <div
      v-for="review in reviews"
      :key="review.review_id"
      class="review"
    >
      <strong>
        ⭐ {{ review.rating }}/5
      </strong>

      <p>
        {{ review.review_text }}
      </p>
    </div>
  </div>

  <div
    v-else
    class="no-reviews"
  >
    No reviews yet.
  </div>

</section>

</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  reviews:{
    type:Array,
    default:()=>[]
  }
});

const emit = defineEmits([
    "review-added"
]);

const showForm = ref(false);

const newReview = ref({
  rating:5,
  review_text:""
});


function submitReview(){
  if(!newReview.value.review_text.trim()){
    return;
  }

  emit(
    "review-added",
    {
      rating:newReview.value.rating,
      review_text:newReview.value.review_text
    }
  );

  newReview.value = {
    rating:5,
    review_text:""
  };

  showForm.value=false;
}
</script>


<style scoped>

.reviews-section{
  margin-top:25px;
}

h2{
  color:#2C2C2C;
  margin-bottom:20px;
}

.review{
  margin-top:20px;
  padding:15px;
  background:#FAFAFA;
  border-radius:10px;
}

.review strong{
  color:#8B5A3C;
}

.review p{
  margin-top:10px;
  color:#555;
  line-height:1.6;
}

.no-reviews{
  padding:15px;
  background:#FAFAFA;
  border-radius:10px;
  color:#666;
}

.reviews-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.add-review-btn{
  width:40px;
  height:40px;
  border-radius:50%;
  background:#8B5A3C;
  color:white;
  font-size:24px;
  border:none;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center;
}

.review-form{
    background:#FAFAFA;
    padding:20px;
    border-radius:12px;
    margin:20px 0;
}

.review-form textarea{
    width:100%;
    min-height:100px;
    margin:15px 0;
    padding:10px;
    border-radius:8px;
    border:1px solid #ddd;
}

.submit-btn{
    background:#8B5A3C;
    color:white;
    border:none;
    padding:12px 20px;
    border-radius:10px;
}

</style>