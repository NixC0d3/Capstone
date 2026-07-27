<template>

  <div class="dashboard">
    <TrendScore
      :report="currentReport"
    />

    <PerformanceSummary
      :report="currentReport"
      organisationType="charity"
    />

    <EngagementChart
      :report="currentReport"
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

const reports = ref([])
const currentReport = ref({
  total_views: 0,
  total_saves: 0,
  total_messages: 0,
  total_reviews: 0,
  total_volunteer_signups: 0,

  profile_views: 0,
  saves: 0,
  messages: 0,
  volunteer_signups: 0,

  average_rating: 0,
  bayesian_rating: 0,
  engagement_score: 0,
  trend_score: 0,
  growth_rate: 0,

  trend_status: "No Data"
})

onMounted(async () => {
  try {
    reports.value = await api.getMonthlyReport(organisationId)
    if (reports.value.length > 0) {
      currentReport.value = reports.value[reports.value.length - 1]
    }
  } catch (error) {
    console.error("Failed to load report:", error)
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
