<template>
  <svg
    class="spinner"
    viewBox="0 0 100 100"
    width="100"
    height="100"
  >
    <circle
      v-for="i in dotCount"
      :key="i"
      :r="dotRadius"
      :cx="getDotPosition(i - 1).x"
      :cy="getDotPosition(i - 1).y"
      fill="#fff"
      :style="{ animationDelay: `${i * 0.1}s` }"
      class="dot"
    />
  </svg>
</template>

<script setup lang="ts">
const dotCount = 10;
const dotRadius = 4;
const radius = 25; // 回転円の半径
const center = 50;

function getDotPosition(index: number) {
  const angle = (2 * Math.PI * index) / dotCount;
  const x = center + radius * Math.cos(angle);
  const y = center + radius * Math.sin(angle);
  return { x, y };
}
</script>

<style scoped>
.spinner {
  animation: rotate 3s linear infinite;
}

.dot {
  opacity: 0.6;
  transform-origin: 50% 50%;
  animation: pulse 1s infinite ease-in-out;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%,
  100% {
    r: 4;
    opacity: 0;
  }
  50% {
    r: 4;
    opacity: 1;
  }
}
</style>
