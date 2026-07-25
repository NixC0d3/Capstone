<template>

  <div class="dashboard" v-if="currentReport">
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
  <p v-else>
    Loading dashboard...
  </p>

</template>

<script setup>

import {ref,onMounted} from "vue"
import {api} from "@/services/api"

import TrendScore from "@/components/AnalyticsDashboard/TrendScore.vue"
import PerformanceSummary from "@/components/AnalyticsDashboard/PerformanceSummary.vue"
import EngagementChart from "@/components/AnalyticsDashboard/EngagementChart.vue"

const reports = ref([])
const currentReport = ref(null)

const organisationId = 15

// TODO: Replace hardcoded organisation ID with the logged-in user's
// organisation after JWT authentication is implemented.
onMounted(async () => {
  try {
    reports.value = await api.getMonthlyReport(organisationId)
    currentReport.value = reports.value[reports.value.length - 1]
    
  }catch (error) {
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
