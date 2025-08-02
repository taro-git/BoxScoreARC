<template>
    <div :style="{ 'background-color': 'white' }">
        <router-link :to="{ name: 'game', params: { gameId: gameSummary.gameId } }" class="card" @click="selectGame">
            <div class="status">{{ gameSummary.statusText }}</div>
            <div v-if="fullView" class="category">{{ gameSummary.gameCategory }}</div>
            <div class="teams">
                <div class="team">
                    <img :src="gameSummary.awayTeam.logo" width="50" />
                    <div v-if="fullView">{{ gameSummary.awayTeam.abbreviation }}</div>
                </div>
                <div v-if="scoreDisplay" class="score">{{ gameSummary.awayScore ?? 0 }}</div>
                <div class="vs">-</div>
                <div v-if="scoreDisplay" class="score">{{ gameSummary.homeScore ?? 0 }}</div>
                <div class="team">
                    <img :src="gameSummary.homeTeam.logo" width="50" />
                    <div v-if="fullView">{{ gameSummary.homeTeam.abbreviation }}</div>
                </div>
            </div>
        </router-link>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

import { gameStore } from '../store/game';

import { GameSummary } from '../types/GameSummary';

const props = defineProps<{
    gameSummary: GameSummary
    scoreDisplay: boolean
    fullView: boolean
}>()

const selectedGame = gameStore()

const selectGame = () => {
    Object.assign(selectedGame.gameSummary, props.gameSummary)
}

</script>

<style scoped>
.card {
    background: white;
    color: black;
    text-decoration: none;
    /* margin: 7px 14px; */
    border-radius: 12px;
    padding: 15px;
    /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); */
    /* 任意：少し立体感を出す */
    /* width: 100%; */
}

.status {
    font-size: 20px;
    text-align: center;
    font-weight: bold;
}

.category {
    font-size: 10px;
    text-align: center;
}

.teams {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0px 15px
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
