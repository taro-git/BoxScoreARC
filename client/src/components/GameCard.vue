<template>
    <div :style="{ 'background-color': disableLink ? 'darken' : 'white' }">
        <router-link :to="{ name: RouteName.Game, params: { gameId: gameSummary.gameId } }" class="card"
            @click="selectGame">
            <div class="status">{{ statusText }}</div>
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
import { ref } from 'vue'

import { RouteName } from '../router/index'
import { gameStore } from '../store/game';
import { GameSummary } from '../types/GameSummary';

const props = defineProps<{
    gameSummary: GameSummary
    scoreDisplay: boolean
    fullView: boolean
    gameDateDisplay: boolean
    disableLink: boolean
}>()

const selectedGame = gameStore()

const statusText = ref(props.gameSummary.statusText)
if (!props.scoreDisplay && props.gameSummary.statusId == 3) {
    statusText.value = 'Final'
}
if (props.gameSummary.statusId == 1) {
    const year = props.gameSummary.gameDatetime.getFullYear()
    const month = props.gameSummary.gameDatetime.getMonth() + 1
    const date = props.gameSummary.gameDatetime.getDate()
    const hour = props.gameSummary.gameDatetime.getHours().toString().padStart(2, '0')
    const minute = props.gameSummary.gameDatetime.getMinutes().toString().padStart(2, '0')
    if (props.gameDateDisplay) {
        statusText.value = `${year}/${month}/${date} ${hour}:${minute}`
    } else {
        statusText.value = `${hour}:${minute}`
    }
} else if (props.gameDateDisplay) {
    statusText.value = `${props.gameSummary.statusText} at ${props.gameSummary.gameDatetime.getFullYear()}/${props.gameSummary.gameDatetime.getMonth() + 1}/${props.gameSummary.gameDatetime.getDate()}`
}

const selectGame = () => {
    Object.assign(selectedGame.gameSummary, props.gameSummary)
}

</script>

<style scoped>
.card {
    color: black;
    text-decoration: none;
    border-radius: 12px;
    padding: 15px;
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
