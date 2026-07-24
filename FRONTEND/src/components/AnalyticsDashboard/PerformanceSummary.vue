<template>

    <div class="summary-card">
        <h3>Performance Summary</h3>

        <div class="summary">

            <div class="item">
                <span>Bayesian Rating</span>
                <strong>{{ report.bayesian_rating.toFixed(1) }}/5</strong>
            </div>

            <div class="item">
                <span>Total Reviews</span>
                <strong>{{ report.total_reviews }}</strong>
            </div>

            <div class="item">
                <span>Profile Views</span>
                <strong>{{ report.profile_views }}</strong>
            </div>

            <div class="item">
                <span>Saves</span>
                <strong>{{ report.saves }}</strong>
            </div>

            <div class="item">
                <span>Messages</span>
                <strong>{{ report.messages }}</strong>
            </div>

            <div v-if="organisationType === 'charity'" 
            class="item">
                <span>Volunteer Sign-ups</span>
                <strong>{{ report.volunteer_signups }}</strong>
            </div>
        </div>
    </div>

</template>

<script setup>

defineProps({
    report:{
        type:Object,
        required:true
    },
    organisationType:{
        type:String,
        required:true
    }
})

</script>

<style scoped>
.summary-card{
    margin-top:30px;
    background:white;
    border-radius:18px;
    padding:30px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}

.summary{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:20px;
}

.item{
  display:flex;
  justify-content:space-between;
  border-bottom:1px solid #eee;
  padding:10px 0;
}

h2{
  margin-bottom:10px;
}

h3{
  margin-top:20px;
}

@media(max-width:700px){
    .summary{
    grid-template-columns:1fr;
    }
}

</style>