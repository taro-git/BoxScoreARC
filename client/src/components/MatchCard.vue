<template>
  <div class="card">
    <div class="status">{{ matchSummary.status_text }}</div>
    <div class="teams">
      <div class="team">
        <img :src="matchSummary.away_logo" width="50" />
        <div>{{ matchSummary.away_team }}</div>
      </div>
      <div v-if="scoreDisplay" class="score">{{ matchSummary.away_score ?? 0 }}</div>
      <div class="vs">-</div>
      <div v-if="scoreDisplay" class="score">{{ matchSummary.home_score ?? 0 }}</div>
      <div class="team">
        <img :src="matchSummary.home_logo" width="50" />
        <div>{{ matchSummary.home_team }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

import type { MatchSummary } from '@/types/MatchSummary';

defineProps<{ 
  matchSummary: MatchSummary
  scoreDisplay: boolean
 }>()
</script>

<style scoped>
.card {
  background: white;
  color: black;
  margin: 7px 14px;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 任意：少し立体感を出す */
}

.status {
  font-size: 20px;
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

.score {
  font-size: 30px;
  color: #363636;
  font-weight: bold;
  text-align: center;
}

.vs {
  font-size: 30px;
  color: #888;
  padding: 0 8px;
}
</style>
