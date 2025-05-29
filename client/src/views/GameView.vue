<template>
  <div class="container">
    <GameCard v-if="!isLoading" :game-summary="gameSummary" :score-display="true" :full-view="false"/>
    <div class="tab-menu">
      <div @click="activeTab = 'teamstats'" :class="['tab', activeTab === 'teamstats' ? 'selected' : '']">Team Stats</div>
      <div @click="activeTab = 'boxscore'" :class="['tab', activeTab === 'boxscore' ? 'selected' : '']">Box Score</div>
      <div @click="activeTab = 'headtoheadrecord'" :class="['tab', activeTab === 'headtoheadrecord' ? 'selected' : '']">Head to Head Record</div>
    </div>
    <component
      v-if="!isLoading"
      :is="currentTabComponent"
      v-bind="currentTabProps"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps } from 'vue'

import TeamStats from '@/components/TeamStats.vue'
import BoxScore from '@/components/BoxScore.vue'
import HeadToHeadRecord from '@/components/HeadToHeadRecord.vue'
import GameCard from '@/components/GameCard.vue'

import { CacheService } from '@/services/cacheService'
import { getBoxScoreSummary, isBoxScoreSummary } from '@/services/getBoxScoreService'

import { BoxScoreSummary } from '@/types/BoxScoreSummary'

const props = defineProps<{
  gameId: string
}>()

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
      onUpdateGameClockRange: updateGameClockRange,
    }
  }
})

function updateGameClockRange(home: number, away: number) {
  gameSummary.value.home_score = home
  gameSummary.value.away_score = away
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

</style>
