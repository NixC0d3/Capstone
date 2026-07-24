<template>
  <div class="trend-card">

    <h2>{{ report?.month }}</h2>

    <div class="trend-row">

      <div class="score">
        <span class="label">Trend Score:</span>
        <span class="value">{{ Math.round(report?.trend_score || 0) }}/100</span>
      </div>

      <div
        class="status"
        :class="report.trend_status?.toLowerCase()"
      >
        <span v-if="report.trend_status === 'Improving'">
          ▲ Improving (+{{ report.growth_rate.toFixed(1) }}%)
        </span>

        <span v-else-if="report.trend_status === 'Declining'">
          ▼ Declining ({{ report.growth_rate.toFixed(1) }}%)
        </span>

        <span v-else>
          ➜ Stable ({{ report.growth_rate.toFixed(1) }}%)
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>

defineProps({
  report:{
    type:Object,
    required:false,
    default:null
  }
})

</script>

<style scoped>

.trend-card{
  background:white;
  border-radius:18px;
  padding:30px;
  box-shadow:0 10px 25px rgba(0,0,0,.08);
}

h2{
  margin:0;
  color:#2C2C2C;
}

.trend-row{
  display:flex;
  justify-content:space-between;
  align-items:center;
  flex-wrap:wrap;
  gap:20px;
}

.score{
  display:flex;
  align-items:baseline;
  gap:10px;
}

.label{
  font-size:1.3rem;
  font-weight:600;
  color:#2C2C2C;
}

.value{
  font-size:2.4rem;
  font-weight:bold;
  color:#8B5A3C;
}

.status{
  font-size:1.2rem;
  font-weight:600;
}

.improving{
  color:#2E8B57;
}

.declining{
  color:#C0392B;
}

.stable{
  color:#666;
}

@media (max-width:700px){
  .trend-row{
    flex-direction:column;
    align-items:flex-start;
  }
}

</style>