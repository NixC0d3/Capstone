<template>
  <div class="trend-card">
    <div class="trend-left">
      <template v-if="generated">
        <span class="label">Trend Score:</span>
        <span class="value">{{ Math.round(report?.trend_score || 0) }}/100</span>
      </template>

      <template v-else>
        <span class="label">Current Month:</span>
        <span class="value small-value">{{ report?.current_month_label || "Current Month" }}</span>
      </template>
    </div>

    <div class="trend-right">
      <div
        v-if="generated"
        class="status"
        :class="trendStatus.toLowerCase()"
      >
        <span v-if="trendStatus === 'Improving'">
          ↗ Improving (+{{ growthRate }}%)
        </span>

        <span v-else-if="trendStatus === 'Declining'">
          ↘ Declining ({{ growthRate }}%)
        </span>

        <span v-else>
          → Stable ({{ growthRate }}%)
        </span>
      </div>

      <div v-else class="helper-text">
        Generate report to compare with previous month
      </div>

      <button
        class="generate-btn"
        @click="$emit('generate-report')"
        :disabled="loading"
      >
        {{ loading ? "Generating..." : generated ? "Refresh Report" : "Generate Report" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  report: {
    type: Object,
    required: false,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  generated: {
    type: Boolean,
    default: false
  }
});

defineEmits(["generate-report"]);

const trendStatus = computed(() => {
  return props.report?.trend_label || props.report?.trend_status || "Stable";
});

const growthRate = computed(() => {
  const value = props.report?.growth_rate || 0;
  return Number(value).toFixed(1);
});
</script>

<style scoped>
.trend-card {
  background: white;
  border-radius: 18px;
  padding: 30px;
  box-shadow: 0 10px 25px rgba(0,0,0,.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 25px;
}

.trend-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.label {
  font-size: 1.4rem;
  font-weight: 700;
  color: #2C2C2C;
}

.value {
  font-size: 2.6rem;
  font-weight: bold;
  color: #8B5A3C;
}

.small-value {
  font-size: 2.2rem;
}

.trend-right {
  display: flex;
  align-items: center;
  gap: 18px;
}

.status {
  font-size: 1.2rem;
  font-weight: 700;
}

.improving {
  color: #2E8B57;
}

.declining {
  color: #C0392B;
}

.stable {
  color: #666;
}

.helper-text {
  color: #666;
  font-weight: 600;
}

.generate-btn {
  border: none;
  background: #8B5A3C;
  color: white;
  padding: 12px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.generate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 700px) {
  .trend-card,
  .trend-right {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
