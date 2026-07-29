<template>
  <main class="business-home">
    <TrendScore
      :report="currentReport"
      :loading="loading"
      :generated="reportGenerated"
      @generate-report="generateReport"
    />

    <PerformanceSummary
      v-if="currentReport"
      :report="currentReport"
      organisationType="business"
      :generated="reportGenerated"
    />

    <div v-else class="loading-message">
      Loading business dashboard...
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "@/services/api";

import TrendScore from "@/components/AnalyticsDashboard/TrendScore.vue";
import PerformanceSummary from "@/components/AnalyticsDashboard/PerformanceSummary.vue";

const loading = ref(false);
const reportGenerated = ref(false);

const currentReport = ref({
  organisation_type: "business",
  trend_score: 0,
  growth_rate: 0,
  trend_label: "Stable",
  trend_status: "Stable",

  previous_month_label: "Previous Month",
  current_month_label: "Current Month",

  previous_month: {
    profile_views: 0,
    saves: 0,
    messages: 0,
    reviews: 0,
    volunteer_signups: 0
  },

  current_month: {
    profile_views: 0,
    saves: 0,
    messages: 0,
    reviews: 0,
    volunteer_signups: 0
  },

  bayesian_rating: 0,
  total_reviews: 0
});

async function loadDashboard(markAsGenerated = false) {
  loading.value = true;

  try {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const userId = user.user_id || user.id;

    if (!userId) {
      console.error("No logged-in business user found.");
      return;
    }

    const organisation = await api.getOwnerOrganisation(userId);

    if (!organisation || !organisation.organisation_id) {
      console.error("No business organisation found for this user.");
      return;
    }

    const data = await api.getOrganisationDashboardReport(
      organisation.organisation_id
    );

    currentReport.value = {
      ...currentReport.value,
      ...data,
      organisation_type: "business"
    };

    if (markAsGenerated) {
      reportGenerated.value = true;
    }

  } catch (error) {
    console.error("Failed to load business dashboard report:", error);
  } finally {
    loading.value = false;
  }
}

function generateReport() {
  loadDashboard(true);
}

onMounted(() => {
  // Loads current-month data only in the interface.
  // It does not show the trend comparison until Generate Report is clicked.
  loadDashboard(false);
});
</script>

<style scoped>
.business-home {
  display: grid;
  gap: 30px;
  padding: 40px;
  background: #f7f6f4;
  min-height: 100vh;
}

.loading-message {
  background: white;
  border-radius: 18px;
  padding: 30px;
  color: #666;
}
</style>
