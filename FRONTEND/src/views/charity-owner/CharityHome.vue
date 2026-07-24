<template>

    <div class="dashboard">

        <TrendScore
            :report="report"
        />

        <PerformanceSummary
            :report="report"
            organisationType="'charity'"
        />

        <EngagementChart
            :report="report"
            organisationType="charity"
        />

    </div>

</template>

<script setup>

import {ref,onMounted} from "vue"
import {api} from "@/services/api"

import TrendScore from "@/components/AnalyticsDashboard/TrendScore.vue"
import PerformanceSummary from "@/components/AnalyticsDashboard/PerformanceSummary.vue"
import EngagementChart from "@/components/AnalyticsDashboard/EngagementChart.vue"

const report = ref(null)

// TODO: Replace hardcoded organisation ID with the logged-in user's
// organisation after JWT authentication is implemented.
onMounted(async () => {
  try {
    report.value = await api.getTrendReport(
      6, // Temporary organisation ID
      7,
      2026
    )
  } catch (error) {
    console.error(error)
  }
})


</script>

<style scoped>
.dashboard{
    display:grid;
    gap:30px;
    padding:40px;
}
</style>