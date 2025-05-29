<template>
  <div class="teams">
    <div @click="selectedTeam='away'" :class="['team', selectedTeam === 'away' ? 'selected' : '']">{{ boxScoreSummary.away.abbreviation }}</div>
    <div @click="selectedTeam='home'" :class="['team', selectedTeam === 'home' ? 'selected' : '']">{{ boxScoreSummary.home.abbreviation }}</div>
  </div>
  <div class="game-clock">
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
  <div class="table-container">
    <table class="fixed-table">
      <thead>
        <tr>
          <th class="left top-row-1 z-high">PLAYER</th>
          <th
            v-for="(col, colIndex) in columns"
            :key="'head1-' + colIndex"
            class="top-row-1"
          >
            {{ col }}
          </th>
        </tr>

        <tr>
          <th
            class="left top-row-2 z-high"
          >
            STARTERS
          </th>
          <th
            class="top-row-2"
            :colspan="columns.length"
          >
          </th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="(row, rowIndex) in rows"
          :key="'row-' + rowIndex"
        >
          <template v-if="rowIndex === 5">
            <th
              class="left top-row-3 z-high"
            >
              BENCH
            </th>
            <th
              class="top-row-3"
              :colspan="columns.length"
            >
            </th>
          </template>

          <template v-else>
            <th :class="['left-data', [rowIndex%2 !== 0 ? 'odd-row' : '']]">
              {{ row.player_name }}
            </th>
            
            <td
              :class="['data', [rowIndex%2 !== 0 ? 'odd-row' : '']]"
            >
              {{ row.pos }}
            </td>
            <td
              :class="['data', [rowIndex%2 !== 0 ? 'odd-row' : '']]"
              v-for="(cell, colIndex) in row.comulative_boxscore"
              :key="'cell-' + rowIndex + '-' + colIndex"
            >
              {{ cell }}
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

import { computed, defineEmits, defineProps, ref, watch } from 'vue'

import { BOX_SCORE_COLUMNS, BoxScore, BoxScoreRow } from '@/types/BoxScore'
import { BoxScoreSummary, Player } from '@/types/BoxScoreSummary';

const props = defineProps<{
  boxScoreSummary: BoxScoreSummary
}>()

const emit = defineEmits<{
  (e: 'updateGameClockRange', home_score: number, away_score: number): void
}>()

const selectedTeam = ref<'home' | 'away'>('away')

const maxMilliSeconds = (12 * 4 + 5 * 2) * 60 * 1000

const gameClockRange = ref([0,0])
watch(gameClockRange, ([start_range, end_range]) => {
  emit('updateGameClockRange', end_range, start_range)
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

const columns = BOX_SCORE_COLUMNS

const convertPlayersToBoxScore = (players: Player[]): BoxScoreRow[] => {
  let boxScoreRows = players.map((player) => ({
    player_id: player.player_id,
    player_name: player.name,
    pos: player.position,
    comulative_boxscore: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
  }))
  boxScoreRows.splice(5, 0, {
    player_id: 0,
    player_name: 'no data',
    pos: '',
    comulative_boxscore: []
  })
  return boxScoreRows
}

const boxScore = ref<BoxScore>({
  home: convertPlayersToBoxScore(props.boxScoreSummary.home.players),
  away: convertPlayersToBoxScore(props.boxScoreSummary.away.players)
})

const rows = computed(() => {
  return selectedTeam.value === 'home' ? boxScore.value.home : boxScore.value.away
})

</script>

<style scoped>

.teams {
  width: 100vw - 80px;
  display: flex;
  margin: 20px 40px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
}
.team {
  flex: 1;
  display: grid;
  text-align: center;
  align-items: center;
  height: 20px;
  font-size: 12px;
}
.selected {
  background-color: rgb(0, 158, 221);
  border-radius: 6px;
}

.game-clock {
  width: 100vw - 100px;
  display: flex;
  flex-direction: column;
  margin: 0px 50px 20px 50px;
  align-items: center;
}
.game-clock-slider {
  width: 100% !important;
  user-select: auto !important;
}

.table-container {
  max-width: 100%;
  color: black;
  overflow: auto;
  border: 1px solid #ccc;
}

.table-container::-webkit-scrollbar {
  display: none;
}

.fixed-table {
  border-collapse: collapse;
}

.fixed-table th,
.fixed-table td {
  padding: 6px 10px;
  text-align: center;
  white-space: nowrap;
}

.top-row-1 {
  position: sticky;
  top: 0;
  z-index: 2;
  padding: 0 !important;
  height: 20px;
  box-sizing: border-box;
  background-color: rgb(0, 48, 136);
  color: white;
  font-size: 10px;
}

.top-row-2 {
  position: sticky;
  top: 20px;
  z-index: 2;
  padding: 0  !important;
  height: 15px;
  box-sizing: border-box;
  font-size: 10px;
  background-color: #999999;
}

.top-row-3 {
  position: sticky;
  top: 35px;
  padding: 0  !important;
  height: 15px;
  box-sizing: border-box;
  font-size: 10px;
  background-color: #999999;
}

.z-high {
  z-index: 3;
}

.left {
  position: sticky;
  left: 0;
}

.left-data {
  position: sticky;
  left: 0;
  background-color: white;
}

.data {
  z-index: 1;
  background-color: white;
}

.odd-row {
  background-color: #f1f1f1;
}

</style>
