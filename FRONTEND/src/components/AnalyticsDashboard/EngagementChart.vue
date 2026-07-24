<template>

<div class="chart-card">

    <h3>Engagement Breakdown</h3>

    <div class="bars">

        <div class="bar-item">

            <span>
                Profile Views
            </span>

            <div class="bar">
                <div
                class="fill"
                :style="{width: calculateWidth(report.profile_views) }"
                ></div>
            </div>

            <strong>
                {{ report.profile_views }}
            </strong>

        </div>

        <div class="bar-item">

            <span>
                Saves
            </span>

            <div class="bar">
                <div
                class="fill"
                :style="{width: calculateWidth(report.saves) }"
                ></div>
            </div>

            <strong>
                {{ report.saves }}
            </strong>

        </div>

        <div class="bar-item">

            <span>
                Messages
            </span>

            <div class="bar">
                <div
                class="fill"
                :style="{width: calculateWidth(report.messages) }"
                ></div>
            </div>

            <strong>
                {{ report.messages }}
            </strong>
        </div>

        <div class="bar-item">
            <span>
                Reviews
            </span>

            <div class="bar">
                <div
                class="fill"
                :style="{width: calculateWidth(report.total_reviews) }"
                ></div>
            </div>

            <strong>
                {{ report.total_reviews }}
            </strong>

        </div>

        <!-- Charity only -->
        <div 
        v-if="organisationType === 'charity'"
        class="bar-item"
        >
            <span>
                Volunteer Sign-ups
            </span>

            <div class="bar">
                <div
                class="fill"
                :style="{width: calculateWidth(report.volunteer_signups) }"
                ></div>
            </div>

            <strong>
                {{ report.volunteer_signups }}
            </strong>
        </div>

    </div>
</div>

</template>


<script setup>

const props = defineProps({
    report:{
        type:Object,
        required:true
    },
    organisationType:{
        type:String,
        required:true
    }
});

function calculateWidth(value){
    const max = Math.max(
        props.report.profile_views,
        props.report.saves,
        props.report.messages,
        props.report.total_reviews,
        props.report.volunteer_signups || 0
    );
    if(max === 0){
        return "0%";
    }
    return `${(value / max) * 100}%`;
}

</script>


<style scoped>

.chart-card{
    margin-top:30px;
    background:white;
    padding:30px;
    border-radius:18px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}

h3{
    margin-bottom:25px;
}

.bar-item{
    display:grid;
    grid-template-columns:150px 1fr 60px;
    align-items:center;
    gap:15px;
    margin-bottom:20px;
}

.bar{
    height:12px;
    background:#eee;
    border-radius:10px;
    overflow:hidden;
}

.fill{
    height:100%;
    background:#8B5A3C;
    border-radius:10px;
}

strong{
    text-align:right;
}

@media(max-width:700px){
    .bar-item{
        grid-template-columns:1fr;
    }
}

</style>