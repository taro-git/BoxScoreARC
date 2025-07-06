<template>
    <div class="container">
        <header class="header">
            <div>
                <button class="header-button" @click="goToToday">Today</button>
            </div>
            <div>Games</div>
            <div>
                <button class="header-button" @click="showPopup = true">📅</button>
            </div>
        </header>

        <CalendarScroller :selected-date="selectedDate" @update-date="updateDate" />

        <MonthlyCalendar v-if="showPopup" :selected-date="selectedDate" @select="selectDateOnMonthlyCalendar"
            @close="showPopup = false" />

        <div class="game-slider-container" @touchstart="onTouchStart" @touchmove="onTouchMove" @touchend="onTouchEnd">
            <div class="game-page" v-for="dayOffset in gameSummariesSets.dayOffsetsList" :key="dayOffset" :style="{
                transform: `translateX(${offsets[dayOffset]}px)`,
                transition: isSliding ? `transform ${slideAnimationDurationSec}s ease` : 'none',
                overflowY: dayOffset === 0 ? 'auto' : 'hidden'
            }">
                <div class="loading-wrapper" v-if="gameSummariesSets.isLoadingMap.value[dayOffset]">
                    <LoadingSpinner />
                </div>
                <ServerError v-else-if="gameSummariesSets.error.value[dayOffset].isError"
                    :error-message="gameSummariesSets.error.value[dayOffset].errorMessage" />
                <template v-else>
                    <div v-if="gameSummariesSets.gameSummaryMap.value[dayOffset].length === 0" class="no-game">no game
                    </div>
                    <GameCard v-for="(game, j) in gameSummariesSets.gameSummaryMap.value[dayOffset]" :key="j"
                        :game-summary="game" :game-date="selectedDateISOString" :score-display="scoreDisplay"
                        :full-view="true" />
                </template>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

import GameCard from '@/components/GameCard.vue'
import CalendarScroller from '@/components/CalendarScroller.vue'
import MonthlyCalendar from '@/components/MonthlyCalendar.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ServerError from '@/components/ServerError.vue'

import { getGameSummaries, isGameSummary } from '@/services/getGameSummariesService'
import { swipeService } from '@/services/swipeService'
import { CacheService } from '@/services/cacheService'

import { gameDateStore } from '@/store/gameDate'
import { settingsStore } from '@/store/settings'

import type { GameSummary } from '@/types/GameSummary'
import { GameSummariesSets } from '@/types/GameSummariesSets'

const selectedDate = ref(gameDateStore().gameDate)
const selectedDateISOString = computed(() => selectedDate.value.toISOString().slice(0, 10))

const scoreDisplay = settingsStore().scoreDisplay

const showPopup = ref(false)
const numberOfPreviousDays = 1
const numberOfFutureDays = 1
const gameSummariesSets = new GameSummariesSets(numberOfPreviousDays, numberOfFutureDays)

const updateDate = (date: Date) => {
    selectedDate.value = date
    gameDateStore().gameDate = date
}

const selectDateOnMonthlyCalendar = (date: Date) => {
    updateDate(date)
    showPopup.value = false
}

const goToToday = () => {
    updateDate(new Date())
}

const catcheService = new CacheService<GameSummary[]>({
    removalPolicy: 'farthest',
    getDistanceForFarthest: (time) => Math.abs(time - new Date(selectedDate.value).setHours(0, 0, 0, 0)),
    cacheFilter: (_, data: unknown): data is GameSummary[] => {
        if (!Array.isArray(data)) return false
        else if (data.length === 0) return true
        else return data.every(item => isGameSummary(item) && (item as GameSummary).status_id !== 2)
    }
})

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
        gameSummariesSets.gameSummaryMap.value[dayOffset] = []

        // update
        targetDate = new Date(base)
        targetDate.setDate(targetDate.getDate() + dayOffset)

        try {
            const response = await catcheService.getOrFetch(
                new Date(targetDate).setHours(0, 0, 0, 0),
                () => getGameSummaries(targetDate)
            )
            gameSummariesSets.gameSummaryMap.value[dayOffset] = response
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
    updateDate(new Date(selectedDate.value.getTime() + 86400000))
}

const slideToPreviousDay = () => {
    updateDate(new Date(selectedDate.value.getTime() - 86400000))
}

const {
    offsets,
    isSliding,
    slideAnimationDurationSec,
    onTouchStart,
    onTouchMove,
    onTouchEnd
} = swipeService(slideToNextDay, slideToPreviousDay, gameSummariesSets.dayOffsetsList.map(dayOffset => {
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

<style scoped>
.container {
    background-color: var(--main-backgroud-color);
    color: #fff;
    height: calc(100% - var(--footer-height));
    display: flex;
    flex-direction: column;
}

.header {
    display: flex;
    justify-content: space-between;
    padding: 12px 0px;
    font-size: 20px;
    align-items: center;
}

.header-button {
    background: none;
    border: none;
    color: #fff;
    font-size: 20px;
    width: 70px;
    align-items: center;
    cursor: pointer;
}

.game-slider-container {
    flex: 1;
    overflow-x: hidden;
    position: relative;
}

.game-slider-container::-webkit-scrollbar {
    display: none;
}

.game-page {
    width: 100vw;
    height: 100%;
    box-sizing: border-box;
    will-change: transform;
    display: flex;
    flex-direction: column;
    position: absolute;
    overflow-x: hidden;
}

.loading-wrapper {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.no-game {
    margin-top: 10px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}
</style>
