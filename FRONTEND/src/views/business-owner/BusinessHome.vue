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
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const userId = user.user_id || user.id;

    if (!userId) {
      console.error("No logged-in business user found.");
      return;
    }

    const data = await api.getBusinessDashboardReport(userId);

    console.log("Business dashboard report:", data);

    currentReport.value = {
      ...currentReport.value,
      ...data,
      profile_views: data.total_views || 0,
      saves: data.total_saves || 0,
      messages: data.total_messages || 0,
      volunteer_signups: data.total_volunteer_signups || 0
    };
  } catch (error) {
    console.error("Failed to load business dashboard report:", error);
  }
});
</script>

<style scoped>
.business-home {
  padding: 32px;
}
</style>
