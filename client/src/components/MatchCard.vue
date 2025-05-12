<template>
  <div class="card">
    <div class="status">{{ match.status }}</div>
    <div class="teams">
      <div class="team">
        <img :src="match.awayLogo" width="50" />
        <div>{{ match.away }}</div>
      </div>
      <div>-</div>
      <div class="team">
        <img :src="match.homeLogo" width="50" />
        <div>{{ match.home }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

interface Match {
  away: string
  home: string
  status: string
  awayLogo: string
  homeLogo: string
}

defineProps<{ match: Match }>()
</script>

<style scoped>
.card {
  background: white;
  color: black;
  margin: 5px;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 任意：少し立体感を出す */
}

.status {
  text-align: center;
  font-weight: bold;
}
.teams {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.team {
  text-align: center;
}
</style>
