<template>
  <router-link :to="{name: 'game', params: { gameId: gameSummary.game_id }}" class="card">
    <div class="status">{{ gameSummary.status_text }}</div>
    <div class="teams">
      <div class="team">
        <img :src="gameSummary.away_logo" width="50" />
        <div>{{ gameSummary.away_team }}</div>
      </div>
      <div v-if="scoreDisplay" class="score">{{ gameSummary.away_score ?? 0 }}</div>
      <div class="vs">-</div>
      <div v-if="scoreDisplay" class="score">{{ gameSummary.home_score ?? 0 }}</div>
      <div class="team">
        <img :src="gameSummary.home_logo" width="50" />
        <div>{{ gameSummary.home_team }}</div>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

import type { GameSummary } from '@/types/GameSummary';

defineProps<{ 
  gameSummary: GameSummary
  scoreDisplay: boolean
 }>()
</script>

<style scoped>
.card {
  background: white;
  color: black;
  text-decoration: none;
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
