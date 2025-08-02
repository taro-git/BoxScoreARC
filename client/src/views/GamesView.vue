<template>
    <v-container class="d-flex flex-column h-100" fluid>

        <CalendarScroller :selected-date="selectedDate" @update-date="updateDate" />

        <v-sheet class="d-flex flex-grow-1 overflow-hidden position-relative bg-base" @touchstart="onTouchStart"
            @touchmove="onTouchMove" @touchend="onTouchEnd">
            <div ref="scroll" class="d-flex flex-column hide-scrollbar"
                v-for="dayOffset in gameSummariesSets.dayOffsetsList" :key="dayOffset" style="
                    width: 100%;
                    height: 100%;
                    position: absolute;
                    overflow-x: hidden;
                    box-sizing: border-box;
                    will-change: transform;
                " :style="{
                    transform: `translateX(${offsets[dayOffset]}px)`,
                    transition: isSliding ? `transform ${slideAnimationDurationSec}s ease` : 'none',
                    overflowY: dayOffset === 0 ? 'auto' : 'hidden'
                }">
                <v-container v-for="(game, j) in gameSummariesSets.gameSummaryMap.value[dayOffset]">
                    <v-skeleton-loader elevation="7" :loading="gameSummariesSets.isLoadingMap.value[dayOffset]"
                        type="image" class="w-100" color="lighten">
                        <v-responsive class="elevation-7 rounded">
                            <GameCard :key="j" :game-summary="game" :score-display="scoreDisplay" :full-view="true" />
                        </v-responsive>
                    </v-skeleton-loader>
                </v-container>
                <v-card
                    v-if="gameSummariesSets.gameSummaryMap.value[dayOffset].length === 0 && !gameSummariesSets.error.value[dayOffset].isError"
                    elevation="0" class="bg-base">
                    <v-card-title class="text-center text-h3 justify-center">no game</v-card-title>
                </v-card>
                <v-empty-state v-if="gameSummariesSets.error.value[dayOffset].isError" title="Whoops, Server Error"
                    :text="gameSummariesSets.error.value[dayOffset].errorMessage" class="text-accent" />
            </div>
        </v-sheet>
    </v-container>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

import { GameSummariesApi } from '../apis/gameSummaries.api'
import GameCard from '../components/GameCard.vue'
import CalendarScroller from '../components/CalendarScroller.vue'
import { swipe } from '../core/swipe'
import { selectedDateStore } from '../store/selectedDate'
import { settingsStore } from '../store/settings'
import { GameSummary } from '../types/GameSummary'
import { GameSummariesSets } from '../types/GameSummariesSets'

const selectedDate = ref(selectedDateStore().selectedDate)

const scoreDisplay = settingsStore().scoreDisplay

const numberOfPreviousDays = 1
const numberOfFutureDays = 1
const gameSummariesSets = new GameSummariesSets(numberOfPreviousDays, numberOfFutureDays)

const updateDate = (date: Date) => {
    const element = scroll.value?.[Math.floor(gameSummariesSets.dayOffsetsList.length / 2)] as HTMLElement | undefined
    if (element) {
        element.scrollTo({ top: 0 })
    }
    selectedDate.value = date
    selectedDateStore().selectedDate = date
}

const scroll = ref<HTMLElement[] | null>(null)

const statusIdPriority = [2, 1, 3]
const gameSummariesApi = new GameSummariesApi()
const updategameSummariesSets = async () => {
    const base = selectedDate.value
    let targetDate: Date
    const sortedDayOffsets = [...gameSummariesSets.dayOffsetsList].sort((a, b) => {
        if (a === 0) return -1
        if (b === 0) return 1
        return a - b
    })

    for (const dayOffset of sortedDayOffsets) {
        // initialize
        gameSummariesSets.isLoadingMap.value[dayOffset] = true
        gameSummariesSets.error.value[dayOffset].isError = false
        gameSummariesSets.error.value[dayOffset].errorMessage = ''
        gameSummariesSets.gameSummaryMap.value[dayOffset] = [new GameSummary()]

        // update
        targetDate = new Date(base)
        targetDate.setDate(targetDate.getDate() + dayOffset)

        try {
            const response = await gameSummariesApi.getGameSummariesByDate(targetDate)
            const sortedResponse = response.sort((a, b) => {
                if (a.statusId !== b.statusId) {
                    return statusIdPriority.indexOf(a.statusId) - statusIdPriority.indexOf(b.statusId)
                }
                if (a.gameDatetime !== b.gameDatetime) {
                    return a.gameDatetime.getTime() - b.gameDatetime.getTime()
                }
                return a.sequence - b.sequence
            })
            gameSummariesSets.gameSummaryMap.value[dayOffset] = sortedResponse
        } catch (error) {
            gameSummariesSets.error.value[dayOffset].isError = true
            gameSummariesSets.error.value[dayOffset].errorMessage =
                error instanceof Error ? error.message : String(error)
        } finally {
            gameSummariesSets.isLoadingMap.value[dayOffset] = false
        }
    }
}


watch(selectedDate, updategameSummariesSets, { immediate: true })

const slideToNextDay = () => {
    updateDate(new Date(new Date(selectedDate.value).getTime() + 86400000))
}

const slideToPreviousDay = () => {
    updateDate(new Date(new Date(selectedDate.value).getTime() - 86400000))
}

const {
    offsets,
    isSliding,
    slideAnimationDurationSec,
    onTouchStart,
    onTouchMove,
    onTouchEnd
} = swipe(slideToNextDay, slideToPreviousDay, gameSummariesSets.dayOffsetsList.map(dayOffset => {
    const windowWidth = window.innerWidth
    return {
        key: dayOffset,
        initialPosition: windowWidth * dayOffset,
        offset: {
            beforeOnSwipeFuncExe: {
                left: -windowWidth,
                right: windowWidth
            },
            afterOnSwipeFuncExe: {
                left: 0,
                right: 0
            }
        }
    }
}))

</script>

<style scoped></style>
