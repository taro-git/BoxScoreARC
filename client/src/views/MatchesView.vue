<template>
  <div class="container">
    <header class="header">
      <div>
        <button class="header-button" @click="goToToday">今日</button>
      </div>
      <div>Matches</div>
      <div>
        <button class="header-button" @click="showPopup = true">&nbsp;📅&nbsp;</button>
      </div>
    </header>

    <CalendarScroller :selected-date="selectedDate" @update-date="updateDate" />

    <MonthlyCalendar
      v-if="showPopup"
      :selected-date="selectedDate"
      @select="onSelectDate"
      @close="showPopup = false"
    />

    <div
      class="match-scroll"
      @touchstart="onTouchStart"
      @touchmove="onTouchMove"
      @touchend="onTouchEnd"
    >
      <div
        class="match-slider"
        :style="{
          transform: `translateX(${sliderOffset}px)`,
          transition: isSliding ? 'transform 0.3s ease' : 'none'
        }"
      >
        <div v-for="(dayMatches, i) in slideMatchSets" :key="i" class="match-page">
          <MatchCard v-for="(match, j) in dayMatches" :key="j" :match="match" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import MatchCard from '@/components/MatchCard.vue'
import CalendarScroller from '@/components/CalendarScroller.vue'
import MonthlyCalendar from '@/components/MonthlyCalendar.vue'

interface Match {
  away: string
  home: string
  status: string
  awayLogo: string
  homeLogo: string
}

const selectedDate = ref(new Date())
const showPopup = ref(false)
const isSliding = ref(false)
const sliderOffset = ref(-window.innerWidth) // 中央を初期表示
const slideMatchSets = ref<Match[][]>([])

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

const getMatchesForDate = (date: Date): Match[] => {
  return Array.from({ length: Math.floor(date.getDate()/5) }, () => ({
    away: 'BOS',
    home: 'NYK',
    status: '試合終了',
    awayLogo: 'https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg',
    homeLogo: 'https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg'
  }))
}

const updateSlideMatchSets = () => {
  const prevDate = new Date(selectedDate.value)
  const nextDate = new Date(selectedDate.value)
  prevDate.setDate(prevDate.getDate() - 1)
  nextDate.setDate(nextDate.getDate() + 1)

  slideMatchSets.value = [
    getMatchesForDate(prevDate),
    getMatchesForDate(selectedDate.value),
    getMatchesForDate(nextDate)
  ]
}

watch(selectedDate, updateSlideMatchSets, { immediate: true })

let startX = 0
const onTouchStart = (e: TouchEvent) => {
  startX = e.touches[0].clientX
  isSliding.value = false
}

const onTouchMove = (e: TouchEvent) => {
  const currentX = e.touches[0].clientX
  sliderOffset.value = -window.innerWidth + (currentX - startX)
}

const onTouchEnd = () => {
  const delta = sliderOffset.value + window.innerWidth

  if (delta < -100) {
    slideToNextDay()
  } else if (delta > 100) {
    slideToPreviousDay()
  } else {
    isSliding.value = true
    sliderOffset.value = -window.innerWidth
  }
}

const slideToNextDay = () => {
  isSliding.value = true
  sliderOffset.value = -window.innerWidth * 2
  setTimeout(() => {
    selectedDate.value = new Date(selectedDate.value.getTime() + 86400000)
    sliderOffset.value = -window.innerWidth
    isSliding.value = false
  }, 300)
}

const slideToPreviousDay = () => {
  isSliding.value = true
  sliderOffset.value = 0
  setTimeout(() => {
    selectedDate.value = new Date(selectedDate.value.getTime() - 86400000)
    sliderOffset.value = -window.innerWidth
    isSliding.value = false
  }, 300)
}
</script>

<style scoped>
.container {
  background-color: #081C45;
  color: white;
  height: calc(100vh - 76px);
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  padding: 12px 20px;
  font-size: 20px;
  align-items: center;
}

.header-button {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.match-scroll {
  flex: 1;
  overflow-x: hidden;
  overflow-y: auto;
  position: relative;
  padding-bottom: 80px;
}

.match-scroll::-webkit-scrollbar {
  display: none;                  /* Chrome, Safari, Opera */
}

.match-slider {
  display: flex;
  width: 300vw;
  will-change: transform;
}

.match-page {
  width: 100vw;
  padding: 0;
  margin-right: 15px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
</style>
