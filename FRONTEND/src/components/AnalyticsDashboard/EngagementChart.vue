<template>
  <div class="engagement-row">
    <div class="bar-track">
      <div
        class="bar-fill"
        :class="barClass"
        :style="{ width: fillWidth + '%' }"
      ></div>
    </div>
    <div class="value">{{ value }}</div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  value: {
    type: Number,
    default: 0
  },
  maxValue: {
    type: Number,
    default: 10
  },
  barClass: {
    type: String,
    default: "current-bar"
  }
});

const safeMax = computed(() => {
  return Math.max(Number(props.maxValue) || 0, 10);
});

const fillWidth = computed(() => {
  const v = Number(props.value) || 0;
  if (v <= 0) return 0;
  return Math.min((v / safeMax.value) * 100, 100);
});
</script>

<style scoped>
.engagement-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.bar-track {
  flex: 1;
  height: 12px;
  background: #ece9e5;
  border-radius: 999px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.3s ease;
}

.current-bar {
  background: #9c623b;
}

.previous-bar {
  background: #b8b1a8;
}

.value {
  min-width: 28px;
  text-align: right;
  font-weight: 700;
  color: #222;
}
</style>
