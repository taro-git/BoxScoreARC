<template>
    <v-sheet class="bg-base hide-scroll d-flex flex-column fill-height">
        <v-btn-toggle v-model="selectedTeam" color="accent" class="justify-center" mandatory>
            <v-col v-for="team in teams" cols="5" class="pa-0">
                <v-btn :value="team" class="bg-darken w-100">{{ gameSummary[team].abbreviation }}</v-btn>
            </v-col>
        </v-btn-toggle>
        <v-skeleton-loader elevation="7" :loading="isLoading" color="lighten" type="table-row@12">
            <v-responsive class="elevation-7 rounded fill-height">
                <box-score-table :game-summary="gameSummary" :data="boxScoreTableData" :selected-team="selectedTeam"
                    :game-clock-range="gameClockRange" />
            </v-responsive>
        </v-skeleton-loader>
    </v-sheet>
</template>

<script setup lang="ts">
import { computed, defineProps, ref, watch } from 'vue'

import { BoxScoreApi } from '../apis/boxScore.api';
import { GameSummariesApi } from '../apis/gameSummaries.api';
import BoxScoreTable from './BoxScoreTable.vue';
import { updateBoxScoreData } from '../core/boxScoreData';
import { gameStore } from '../store/game';
import { BOX_SCORE_COLUMN_KEYS, BoxScore, type BoxScoreTableData } from '../types/BoxScore'
import { Cache } from '../core/cache';

const props = defineProps<{
    gameId: string
    gameClockRange: number[]
}>()

const teams = ['awayTeam', 'homeTeam'] as const
type Teams = typeof teams[number]
const selectedTeam = ref<Teams>('awayTeam')

const game = gameStore()
const gameSummary = game.gameSummary
gameSummary.awayScore = 0
gameSummary.homeScore = 0
watch(props.gameClockRange, ([startRange, endRange]) => {
    boxScoreTableData.value = updateBoxScoreData(boxScoreTableData.value, boxScore.value, startRange, endRange)
    gameSummary.awayScore = gameSummary.awayPlayers.filter(player => !player.isInactive).map(player => player.playerId)
        .reduce((totalPts, playerId) => totalPts + boxScoreTableData.value[playerId][1], 0)
    gameSummary.homeScore = gameSummary.homePlayers.filter(player => !player.isInactive).map(player => player.playerId)
        .reduce((totalPts, playerId) => totalPts + boxScoreTableData.value[playerId][1], 0)
})

const gameSummaryLoading = ref(true)
const boxScoreDataLoading = ref(true)
const isLoading = computed(() => gameSummaryLoading.value || boxScoreDataLoading.value)

const boxScoreTableData = ref<BoxScoreTableData>({})
const gameSummariesApi = new GameSummariesApi()
gameSummariesApi.getGameSummaryByGameId(props.gameId)
    .then((response) => {
        gameSummary.awayTeam = response.awayTeam
        gameSummary.homeTeam = response.homeTeam
        gameSummary.awayPlayers = response.awayPlayers
        gameSummary.homePlayers = response.homePlayers
        const players = [...response.homePlayers, ...response.awayPlayers]
        players.forEach(player => {
            if (!player.isInactive) boxScoreTableData.value[player.playerId] = new Array(BOX_SCORE_COLUMN_KEYS.length - 1).fill(0)
        })
        gameSummaryLoading.value = false
    })

const boxScoreRawDatacacheService = new Cache<BoxScore>({
    ttlSeconds: 900,
    maxItems: 5,
})
const boxScore = ref<BoxScore>(new BoxScore())
const boxScoreApi = new BoxScoreApi()
boxScoreRawDatacacheService.getOrFetch(Number(props.gameId), () => boxScoreApi.getBoxScore(props.gameId))
    .then((response) => {
        boxScore.value = response
        game.finalPeriod = response.finalPeriod
        boxScoreDataLoading.value = false
    })
</script>

<style scoped></style>
