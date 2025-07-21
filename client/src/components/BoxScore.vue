<template>
    <v-sheet class="bg-base hide-scroll d-flex flex-column fill-height">
        <v-btn-toggle v-model="selectedTeam" color="accent" class="justify-center" mandatory>
            <v-col v-for="team in teams" cols="5" class="pa-0">
                <v-btn :value="team" class="bg-darken w-100">{{ boxScoreSummary[team].abbreviation }}</v-btn>
            </v-col>
        </v-btn-toggle>
        <v-skeleton-loader elevation="7" :loading="isLoading" color="lighten" type="table-row@12">
            <v-responsive class="elevation-7 rounded fill-height">
                <box-score-table :box-score-summary="boxScoreSummary" :box-score-data="boxScoreData"
                    :selected-team="selectedTeam" :game-clock-range="gameClockRange" />
            </v-responsive>
        </v-skeleton-loader>
    </v-sheet>
</template>

<script setup lang="ts">
import { computed, defineProps, ref, watch } from 'vue'

import { BoxScoreRawDataApi } from '../apis/boxScoreRawData';
import { BoxScoreSummaryApi } from '../apis/boxScoreSummary';
import BoxScoreTable from './BoxScoreTable.vue';
import { updateBoxScoreData } from '../core/boxScoreData';
import { gameSummaryStore } from '../store/gameSummary';
import { BOX_SCORE_COLUMN_KEYS, type BoxScoreData, type BoxScoreRawData, isBoxScoreRawData } from '../types/BoxScore'
import { BoxScoreSummary, isBoxScoreSummary } from '../types/BoxScoreSummary';
import { Cache } from '../core/cache';

const props = defineProps<{
    gameId: string
    gameClockRange: number[]
}>()

const teams = ['away', 'home'] as const
type Teams = typeof teams[number]
const selectedTeam = ref<Teams>('away')

const gameSummary = gameSummaryStore()
gameSummary.away_score = 0
gameSummary.home_score = 0
watch(props.gameClockRange, ([startRange, endRange]) => {
    boxScoreData.value = updateBoxScoreData(boxScoreData.value, boxScoreRawData.value, startRange, endRange)
    gameSummary.away_score = boxScoreSummary.value.away.players.filter(player => !player.is_inactive).map(player => player.player_id)
        .reduce((total_pts, player_id) => total_pts + boxScoreData.value[player_id][1], 0)
    gameSummary.home_score = boxScoreSummary.value.home.players.filter(player => !player.is_inactive).map(player => player.player_id)
        .reduce((total_pts, player_id) => total_pts + boxScoreData.value[player_id][1], 0)
})

const boxScoreSummaryLoading = ref(true)
const boxScoreDataLoading = ref(true)
const isLoading = computed(() => boxScoreSummaryLoading.value || boxScoreDataLoading.value)

const boxScoreSummarycacheService = new Cache<BoxScoreSummary>({
    ttlSeconds: 900,
    maxItems: 10,
    cacheFilter: (_, data: unknown): data is BoxScoreSummary => isBoxScoreSummary(data),
})

const boxScoreSummary = ref<BoxScoreSummary>(new BoxScoreSummary())

const boxScoreData = ref<BoxScoreData>({})
const boxScoreSummaryApi = new BoxScoreSummaryApi()
boxScoreSummarycacheService.getOrFetch(Number(props.gameId), () => boxScoreSummaryApi.getBoxScoreSummary(props.gameId))
    .then((response) => {
        boxScoreSummary.value = response
        gameSummary.away_logo = response.away.logo
        gameSummary.home_logo = response.home.logo
        const players = [...response.home.players, ...response.away.players]
        players.forEach(player => {
            if (!player.is_inactive) boxScoreData.value[player.player_id] = new Array(BOX_SCORE_COLUMN_KEYS.length - 1).fill(0)
        })
        boxScoreSummaryLoading.value = false
    })

const boxScoreRawDatacacheService = new Cache<BoxScoreRawData>({
    ttlSeconds: 900,
    maxItems: 5,
    cacheFilter: (_, data: unknown): data is BoxScoreRawData => isBoxScoreRawData(data),
})
const boxScoreRawData = ref<BoxScoreRawData>({})
const boxScoreRawDataApi = new BoxScoreRawDataApi()
boxScoreRawDatacacheService.getOrFetch(Number(props.gameId), () => boxScoreRawDataApi.getBoxScoreRawData(props.gameId))
    .then((response) => {
        boxScoreRawData.value = response
        boxScoreDataLoading.value = false
    })
</script>

<style scoped></style>
