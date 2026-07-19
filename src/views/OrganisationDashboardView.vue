<script setup>
import DashboardStatsCard from "@/components/DashboardStatsCard.vue";
import TrendScoreCard from "@/components/TrendScoreCard.vue";
</script>

<template>
  <div class="container">
    <h1>Organisation Dashboard</h1>
    <p class="text-muted">Dashboard for businesses and charities.</p>

    <div class="row g-3">
      <div class="col-md-3">
        <DashboardStatsCard label="Profile Views" value="0" />
      </div>
      <div class="col-md-3">
        <DashboardStatsCard label="Saves" value="0" />
      </div>
      <div class="col-md-3">
        <DashboardStatsCard label="Messages" value="0" />
      </div>
      <div class="col-md-3">
        <TrendScoreCard :trend-score="0" status="Stable" />
      </div>
    </div>
  </div>
</template>
