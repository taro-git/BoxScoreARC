<template>
  <div class="container">
    <header class="header">
      <div>
        <button class="header-button" @click="goToToday">Today</button>
      </div>
      <div>Matches</div>
      <div>
        <button class="header-button" @click="showPopup = true">📅</button>
      </div>
    </header>

    <CalendarScroller :selected-date="selectedDate" @update-date="updateDate" />

    <MonthlyCalendar
      v-if="showPopup"
      :selected-date="selectedDate"
      @select="selectDateOnMonthlyCalendar"
      @close="showPopup = false"
    />

    <div class="match-slider-container" @touchstart="onTouchStart" @touchmove="onTouchMove" @touchend="onTouchEnd">
      <div
        class="match-page"
        v-for="dayOffset in matchSummariesSets.dayOffsetsList"
        :key="dayOffset"
        :style="{
          transform: `translateX(${offsets[dayOffset]}px)`,
          transition: isSliding ? `transform ${slideAnimationDurationSec}s ease` : 'none',
          overflowY: dayOffset === 0 ? 'auto' : 'hidden'
        }"
      >
        <div class="loading-wrapper" v-if="matchSummariesSets.isLoadingMap.value[dayOffset]" >
          <LoadingSpinner />
        </div>
        <ServerError v-else-if="matchSummariesSets.error.value[dayOffset].isError" :error-message="matchSummariesSets.error.value[dayOffset].errorMessage" />
        <template v-else>
          <div v-if="matchSummariesSets.matchSummaryMap.value[dayOffset].length === 0" class="no-game">no game</div>
          <MatchCard
            v-for="(match, j) in matchSummariesSets.matchSummaryMap.value[dayOffset]"
            :key="j"
            :match-summary="match"
            :score-display="true"
          />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

import MatchCard from '@/components/MatchCard.vue'
import CalendarScroller from '@/components/CalendarScroller.vue'
import MonthlyCalendar from '@/components/MonthlyCalendar.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ServerError from '@/components/ServerError.vue'

import { getMatchSummaries, isMatchSummary } from '@/services/getMatchSummariesService'
import { swipeService } from '@/services/swipeService'
import { CacheService } from '@/services/cacheService'

import type { MatchSummary } from '@/types/MatchSummary'
import { MatchSummariesSets } from '@/types/MatchSummariesSets'

const selectedDate = ref(new Date())
const showPopup = ref(false)
const numberOfPreviousDays = 1
const numberOfFutureDays = 1
const matchSummariesSets = new MatchSummariesSets(numberOfPreviousDays, numberOfFutureDays)

const updateDate = (date: Date) => {
  selectedDate.value = date
}

const selectDateOnMonthlyCalendar = (date: Date) => {
  updateDate(date)
  showPopup.value = false
}

const goToToday = () => {
  updateDate(new Date())
}

const catcheService = new CacheService<MatchSummary[]>({
  removalPolicy: 'farthest',
  getDistanceForFarthest: (time) => Math.abs(time - new Date(selectedDate.value).setHours(0, 0, 0, 0)),
  cacheFilter: (_, data: unknown): data is MatchSummary[] => {
    if (!Array.isArray(data)) return false
    else if (data.length === 0) return true
    else return data.every(item => isMatchSummary(item) && (item as MatchSummary).status_id !== 2)
  }
})

const updateMatchSummariesSets = async () => {
  const base = selectedDate.value
  let targetDate: Date
  const sortedDayOffsets = [...matchSummariesSets.dayOffsetsList].sort((a, b) => {
    if (a === 0) return -1
    if (b === 0) return 1
    return a - b
  })

  for (const dayOffset of sortedDayOffsets) {
    // initialize
    matchSummariesSets.isLoadingMap.value[dayOffset] = true
    matchSummariesSets.error.value[dayOffset].isError = false
    matchSummariesSets.error.value[dayOffset].errorMessage = ''
    matchSummariesSets.matchSummaryMap.value[dayOffset] = []

    // update
    targetDate = new Date(base)
    targetDate.setDate(targetDate.getDate() + dayOffset)

    try {
      const response = await catcheService.getOrFetch(
        new Date(targetDate).setHours(0, 0, 0, 0),
        () => getMatchSummaries(targetDate)
      )
      matchSummariesSets.matchSummaryMap.value[dayOffset] = response
    } catch (error) {
      matchSummariesSets.error.value[dayOffset].isError = true
      matchSummariesSets.error.value[dayOffset].errorMessage =
        error instanceof Error ? error.message : String(error)
    } finally {
      matchSummariesSets.isLoadingMap.value[dayOffset] = false
    }
  }
}


watch(selectedDate, updateMatchSummariesSets, { immediate: true })

const slideToNextDay = () => {
  selectedDate.value = new Date(selectedDate.value.getTime() + 86400000)
}

const slideToPreviousDay = () => {
  selectedDate.value = new Date(selectedDate.value.getTime() - 86400000)
}

const {
  offsets,
  isSliding,
  slideAnimationDurationSec,
  onTouchStart,
  onTouchMove,
  onTouchEnd
} = swipeService(slideToNextDay, slideToPreviousDay, matchSummariesSets.dayOffsetsList.map(dayOffset => {
  const windowWidth = window.innerWidth
  return {
    key: dayOffset,
    initialPosition: windowWidth*dayOffset,
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

.match-slider-container {
  flex: 1;
  overflow-x: hidden;
  position: relative;
}

.match-slider-container::-webkit-scrollbar {
  display: none;
}

.match-page {
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
