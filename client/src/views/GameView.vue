<template>
  <div class="container">
    <GameCard v-if="!isLoading" :game-summary="gameSummary" :score-display="true" :full-view="false"/>
    <div class="tab-menu">
      <div @click="activeTab = 'teamstats'" :class="['tab', activeTab === 'teamstats' ? 'selected' : '']">Team Stats</div>
      <div @click="activeTab = 'boxscore'" :class="['tab', activeTab === 'boxscore' ? 'selected' : '']">Box Score</div>
      <div @click="activeTab = 'headtoheadrecord'" :class="['tab', activeTab === 'headtoheadrecord' ? 'selected' : '']">Head to Head Record</div>
    </div>
    <div v-if="activeTab === 'teamstats' || activeTab === 'boxscore'" class="game-clock">
        <label for="game-time">Game Clock Range</label>
        <vue-slider
        class="game-clock-slider"
        v-model="gameClockRange"
        :max="maxMilliSeconds"
        :tooltip="'always'"
        :tooltip-formatter="formatReminTime"
        :height="10"
        />
    </div>
    <component
      v-if="!isLoading"
      :is="currentTabComponent"
      v-bind="currentTabProps"
    />
  </div>
</template>

<script setup lang="ts">
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

import { ref, computed, defineProps, watch } from 'vue'

import TeamStats from '@/components/TeamStats.vue'
import BoxScore from '@/components/BoxScore.vue'
import HeadToHeadRecord from '@/components/HeadToHeadRecord.vue'
import GameCard from '@/components/GameCard.vue'

import { CacheService } from '@/services/cacheService'
import { getBoxScoreSummary, isBoxScoreSummary } from '@/services/getBoxScoreService'

import { BoxScoreSummary } from '@/types/BoxScoreSummary'

const props = defineProps<{
  gameId: string
  gameDate: string
}>()

sessionStorage.setItem('gameDate', props.gameDate)

const activeTab = ref<'teamstats' | 'boxscore' | 'headtoheadrecord'>('boxscore')

const currentTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'teamstats': return TeamStats
    case 'headtoheadrecord': return HeadToHeadRecord
    default: return BoxScore
  }
})

const currentTabProps = computed(() => {
  switch (activeTab.value) {
    case 'teamstats': return {}
    case 'headtoheadrecord': return {}
    default: return { 
      boxScoreSummary: boxScoreSummary.value,
      maxMilliSeconds: maxMilliSeconds,
      gameClockRange: gameClockRange.value,
    }
  }
})

const maxMilliSeconds = (12 * 4 + 5 * 2) * 60 * 1000
const gameClockRange = ref([0,0])
watch(gameClockRange, ([start_range, end_range]) => {
  gameSummary.value.away_score = start_range
  gameSummary.value.home_score = end_range
})

const formatReminTime = (milliSeconds: number) => {
  let nth = ''
  let reminMinutes = 12
  let reminMilliSeconds = 0
  let reminSeconds = 0
  let reminTime = ''
  if (milliSeconds <= 48*60*1000) {
    let quarter = 0
    if (milliSeconds%(12*60*1000) !== 0){
      quarter = Math.floor((milliSeconds) / (12*60*1000)) + 1
    } else {
      if (milliSeconds === 0) {
        quarter = 1
      } else {
        quarter = Math.floor((milliSeconds) / (12*60*1000))
      }
    }
    switch (quarter) {
      case 1:
        nth = '1st Q.'
        break
      case 2:
        nth = '2nd Q.'
        break
      case 3:
        nth = '3rd Q.'
        break
      case 4:
        nth = '4th Q.'
        break
    }
    reminMilliSeconds = quarter*12*60*1000 - milliSeconds
    reminMinutes = Math.floor(reminMilliSeconds / (60*1000))
    reminMilliSeconds = reminMilliSeconds%(60*1000)
  } else {
    const otMilliSeconds = milliSeconds - 48*60*1000
    let ot = 0
    if (otMilliSeconds%(5*60*1000) !== 0){
      ot = Math.floor(otMilliSeconds/ (5*60*1000)) + 1
    } else {
      ot = Math.floor(otMilliSeconds/ (5*60*1000))
    }
    nth = `OT${ot}`
    reminMilliSeconds = ot*5*60*1000 - otMilliSeconds
    reminMinutes = Math.floor(reminMilliSeconds / (60*1000))
    reminMilliSeconds = reminMilliSeconds%(60*1000)
  }
  if (reminMinutes === 0){
    reminSeconds = reminMilliSeconds / 1000
    const roundedReminSeconds = reminSeconds.toFixed(1)
    reminTime = `${roundedReminSeconds} s`
  } else {
    reminSeconds = Math.floor(reminMilliSeconds / 1000)
    const paddedReminMinutes = String(reminMinutes).padStart(2, '0')
    const paddedReminSeconds = String(reminSeconds).padStart(2, '0')
    reminTime = `${paddedReminMinutes}:${paddedReminSeconds}`
  }
  return `${nth} ${reminTime}`
}

let isLoading = ref(true)

const cacheService = new CacheService<BoxScoreSummary>({
  ttlSeconds: 900,
  maxItems: 10,
  cacheFilter: (_, data: unknown): data is BoxScoreSummary => isBoxScoreSummary(data),
})

const boxScoreSummary = ref()
const gameSummary = ref()
cacheService.getOrFetch(Number(props.gameId), () => getBoxScoreSummary(props.gameId))
  .then((response) => {
    boxScoreSummary.value = response
    gameSummary.value = {
      game_id: props.gameId,
      home_logo: response.home.logo,
      home_score: 0,
      away_logo: response.away.logo,
      away_score: 0,
      status_text: response.game_date_jst.toISOString().slice(0, 10),
    }
    isLoading.value = false
  })

</script>


<style scoped>

.container {
  background-color: var(--main-backgroud-color);
  color: #fff;
  height: calc(100% - var(--footer-height));
  display: flex;
  flex-direction: column;
}

.tab-menu {
  display: flex;
}
.tab {
  flex: 1;
  display: grid;
  text-align: center;
  align-items: center;
  color:rgba(255, 255, 255, 0.5);
  font-size: large;
  padding-bottom: 4px;
}
.tab.selected {
  color: rgba(255, 255, 255, 1);
  border-bottom: 4px solid rgba(200, 50, 50, 0.9);
}

.game-clock {
  display: flex;
  flex-direction: column;
  margin: 20px 50px 0px 50px;
  align-items: center;
}
.game-clock-slider {
  width: 100% !important;
  user-select: auto !important;
}

</style>
