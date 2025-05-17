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
      @select="onSelectDate"
      @close="showPopup = false"
    />

    <div class="match-slider-container" @touchstart="onTouchStart" @touchmove="onTouchMove" @touchend="onTouchEnd">
      <div
        class="match-page"
        v-for="(dayMatches, i) in matchSummariesSets"
        :key="i"
        :style="{
          transform: `translateX(${offsets[i]}px)`,
          transition: isSliding ? `transform ${slideAnimationDurationSec}s ease` : 'none',
          overflowY: i === 1 ? 'auto' : 'hidden'
        }"
      >
        <MatchCard
          v-for="(match, j) in dayMatches"
          :key="j"
          :match-summary="match"
          :score-display="true"
        />
        <div v-if="dayMatches.length === 0" class="no-game">no game</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

import MatchCard from '@/components/MatchCard.vue'
import CalendarScroller from '@/components/CalendarScroller.vue'
import MonthlyCalendar from '@/components/MonthlyCalendar.vue'

import { getMatchSummaries } from '@/services/getMatchSummariesService'
import { swipeService } from '@/services/swipeService'
import { CacheService } from '@/services/cacheService'

import type { MatchSummary } from '@/types/MatchSummary'

const selectedDate = ref(new Date())
const showPopup = ref(false)
const matchSummariesSets = ref<MatchSummary[][]>([])

const updateDate = (date: Date) => {
  selectedDate.value = date
}

const onSelectDate = (date: Date) => {
  selectedDate.value = date
  showPopup.value = false
}

const goToToday = () => {
  selectedDate.value = new Date()
}

const catcheService = new CacheService<MatchSummary[]>({
  removalPolicy: 'farthest',
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  getDistanceForFarthest: (time, dummy) => Math.abs(time - selectedDate.value.setHours(0, 0, 0, 0)),
})

const updateMatchSummariesSets = async () => {
  const base = selectedDate.value
  const prev = new Date(base)
  const next = new Date(base)
  prev.setDate(prev.getDate() - 1)
  next.setDate(next.getDate() + 1)

  matchSummariesSets.value = await Promise.all([
    catcheService.getOrFetch(prev.setHours(0, 0, 0, 0), () => getMatchSummaries(prev)),
    catcheService.getOrFetch(base.setHours(0, 0, 0, 0), () => getMatchSummaries(base)),
    catcheService.getOrFetch(next.setHours(0, 0, 0, 0), () => getMatchSummaries(next))
  ])
}

watch(selectedDate, updateMatchSummariesSets, { immediate: true })

const slideToNextDay = () => {
  matchSummariesSets.value = [
    ...matchSummariesSets.value.slice(1),
    []
  ]
  selectedDate.value = new Date(selectedDate.value.getTime() + 86400000)
}

const slideToPreviousDay = () => {
  matchSummariesSets.value = [
    [],
    ...matchSummariesSets.value.slice(0, 2),
  ]
  selectedDate.value = new Date(selectedDate.value.getTime() - 86400000)
}

const temp = -window.innerWidth
const {
  offsets,
  isSliding,
  slideAnimationDurationSec,
  onTouchStart,
  onTouchMove,
  onTouchEnd
} = swipeService(slideToNextDay, slideToPreviousDay, [
  {
    initialPosition: temp,
    offset: {
      beforeOnSwipeFuncExe: {
        left: temp,
        right: -temp
      },
      afterOnSwipeFuncExe: {
        left: 0,
        right: 0
      }
    }
  },
  {
    initialPosition: 0,
    offset: {
      beforeOnSwipeFuncExe: {
        left: temp,
        right: -temp
      },
      afterOnSwipeFuncExe: {
        left: 0,
        right: 0
      }
    }
  },
  {
    initialPosition: -temp,
    offset: {
      beforeOnSwipeFuncExe: {
        left: temp,
        right: -temp
      },
      afterOnSwipeFuncExe: {
        left: 0,
        right: 0
      }
    }
  },
])

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


.no-game {
  text-align: center;
}

</style>
