<template>
  <div class="container">
    <GameCard v-if="isLoading" :game-summary="gameSummary" :score-display="true" :full-view="false"/>
    <div class="tab-menu">
      <div @click="activeTab = 'teamstats'" :class="['tab', activeTab === 'teamstats' ? 'selected' : '']">Team Stats</div>
      <div @click="activeTab = 'boxscore'" :class="['tab', activeTab === 'boxscore' ? 'selected' : '']">Box Score</div>
      <div @click="activeTab = 'headtoheadrecord'" :class="['tab', activeTab === 'headtoheadrecord' ? 'selected' : '']">Head to Head Record</div>
    </div>
    <component :is="currentTabComponent" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps } from 'vue';

import TeamStats from '@/components/TeamStats.vue';
import BoxScore from '@/components/BoxScore.vue';
import HeadToHeadRecord from '@/components/HeadToHeadRecord.vue';
import GameCard from '@/components/GameCard.vue';

import { getGameSummary } from '@/services/getGameSummariesService';

const props = defineProps<{
  gameId: string
}>()

const activeTab = ref<'teamstats' | 'boxscore' | 'headtoheadrecord'>('boxscore');

const currentTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'teamstats': return TeamStats;
    case 'headtoheadrecord': return HeadToHeadRecord;
    default: return BoxScore;
  }
});

let isLoading = ref(false)

const gameSummary = ref()
getGameSummary(props.gameId)
  .then((response) => {
    gameSummary.value = response
    isLoading.value = true
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
