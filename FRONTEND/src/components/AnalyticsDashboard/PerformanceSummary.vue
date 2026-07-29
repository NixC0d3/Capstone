<template>
  <div class="summary-card">
    <div class="header-row">
      <h3>
        {{ generated ? "Monthly Engagement Comparison" : "Engagement Summary" }}
      </h3>

      <div v-if="generated" class="legend">
        <span class="legend-item previous-dot">Previous Month</span>
        <span class="legend-item current-dot">Current Month</span>
      </div>
    </div>

    <div
      v-for="metric in metrics"
      :key="metric.key"
      class="metric-block"
    >
      <h4>{{ metric.label }}</h4>

      <!-- Previous month only shows after Generate Report -->
      <div
        v-if="generated"
        class="bar-row"
      >
        <span class="month-label">Previous</span>

        <div class="bar">
          <div
            class="fill previous-fill"
            :style="{ width: calculateWidth(getPreviousValue(metric.key), metric.key) }"
          ></div>
        </div>

        <strong>{{ getPreviousValue(metric.key) }}</strong>
      </div>

      <!-- Current month row -->
      <div
        class="bar-row"
        :class="{ 'current-only-row': !generated }"
      >
        <span
          v-if="generated"
          class="month-label"
        >
          Current
        </span>

        <div class="bar">
          <div
            class="fill current-fill"
            :style="{ width: calculateWidth(getCurrentValue(metric.key), metric.key) }"
          ></div>
        </div>

        <strong>{{ getCurrentValue(metric.key) }}</strong>
      </div>
    </div>

    <div class="rating-row">
      <div class="rating-item">
        <span>Bayesian Rating</span>
        <strong>{{ Number(report?.bayesian_rating || 0).toFixed(1) }}/5</strong>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  report: {
    type: Object,
    required: true
  },
  organisationType: {
    type: String,
    required: true
  },
  generated: {
    type: Boolean,
    default: false
  }
});

const metrics = computed(() => {
  const list = [
    { key: "profile_views", label: "Profile Views" },
    { key: "saves", label: "Saves" },
    { key: "messages", label: "Messages" },
    { key: "reviews", label: "Reviews" }
  ];

  if (props.organisationType === "charity") {
    list.push({
      key: "volunteer_signups",
      label: "Volunteer Sign-ups"
    });
  }

  return list;
});

function getPreviousValue(key) {
  return Number(props.report?.previous_month?.[key] || 0);
}

function getCurrentValue(key) {
  return Number(props.report?.current_month?.[key] || 0);
}

function calculateWidth(value, key) {
  const previous = props.generated ? getPreviousValue(key) : 0;
  const current = getCurrentValue(key);

  /*
    Minimum max of 10 prevents small values like 1
    from filling the entire bar.
  */
  const max = Math.max(previous, current, 10);

  return `${(value / max) * 100}%`;
}
</script>

<style scoped>
.summary-card {
  margin-top: 30px;
  background: white;
  border-radius: 18px;
  padding: 30px;
  box-shadow: 0 10px 25px rgba(0,0,0,.08);
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 28px;
}

h3 {
  margin: 0;
  color: #2C2C2C;
}

.legend {
  display: flex;
  gap: 14px;
  font-size: 0.9rem;
}

.legend-item {
  font-weight: 600;
}

.previous-dot {
  color: #4f6f88;
}

.current-dot {
  color: #8B5A3C;
}

.metric-block {
  margin-bottom: 26px;
}

.metric-block h4 {
  margin: 0 0 12px;
  color: #2C2C2C;
}

.bar-row {
  display: grid;
  grid-template-columns: 100px 1fr 50px;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.current-only-row {
  grid-template-columns: 1fr 50px;
}

.month-label {
  color: #666;
  font-size: 0.95rem;
}

.bar {
  height: 12px;
  background: #eee;
  border-radius: 10px;
  overflow: hidden;
}

.fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
}

.previous-fill {
  background: #4f6f88;
}

.current-fill {
  background: #8B5A3C;
}

strong {
  text-align: right;
}

.rating-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-top: 30px;
}

.rating-item {
  background: #faf8f5;
  border-radius: 14px;
  padding: 18px;
  display: flex;
  justify-content: space-between;
}

@media(max-width: 700px) {
  .header-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .bar-row,
  .current-only-row {
    grid-template-columns: 1fr;
  }
}
</style>
