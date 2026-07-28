<template>
  <main class="business-home">
    <TrendScore :report="currentReport" />

    <PerformanceSummary :report="currentReport" />

    <EngagementChart :report="currentReport" />
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "@/services/api";

import TrendScore from "@/components/AnalyticsDashboard/TrendScore.vue";
import PerformanceSummary from "@/components/AnalyticsDashboard/PerformanceSummary.vue";
import EngagementChart from "@/components/AnalyticsDashboard/EngagementChart.vue";

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
  trend_status: "Stable"
});

onMounted(async () => {
  try {

    const user = JSON.parse(localStorage.getItem("user"));

    // get the business owned by this user
    const organisation = await api.getOwnerOrganisation(user.user_id);

    // now we know the organisation id
    const reports = await api.getMonthlyReport(organisation.organisation_id);

    if (reports.length > 0) {
      currentReport.value = reports[report.length - 1]
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

   
