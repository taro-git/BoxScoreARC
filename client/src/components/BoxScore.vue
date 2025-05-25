<template>
  <div class="teams">
    <div @click="selectedTeam='home'" :class="['team', selectedTeam === 'home' ? 'selected' : '']">CLE</div>
    <div @click="selectedTeam='away'" :class="['team', selectedTeam === 'away' ? 'selected' : '']">BOS</div>
  </div>
  <div class="game-clock">
    <label for="game-time">試合時間: {{ formattedTime }}</label>
    <input
      id="game-time"
      type="range"
      class="game-clock-slider"
      min="0"
      :max="maxSeconds"
      v-model="timeInSeconds"
      step="1"
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
              {{ row.label }}
            </th>
            <td
              :class="['data', [rowIndex%2 !== 0 ? 'odd-row' : '']]"
              v-for="(cell, colIndex) in row.data"
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
import { computed, ref } from 'vue'

const selectedTeam = ref<'home' | 'away'>('home')



// 最大 48分（NBAの1試合）
const maxSeconds = 48 * 60

// 秒単位でバインディング
const timeInSeconds = ref(0)

// mm:ss 形式に整形
const formattedTime = computed(() => {
  const minutes = Math.floor(timeInSeconds.value / 60)
  const seconds = timeInSeconds.value % 60
  const paddedSeconds = seconds.toString().padStart(2, '0')
  return `${minutes}:${paddedSeconds}`
})

interface Row {
  label: string
  data: string[]
}

const columns: string[] = [
  'POS', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG', 'FG%', '3P', '3P%', 'FT', 'FT%', 'OREB', 'DREB', 'TO', 'PF', 'EFF', '+/-'
]

const rows: Row[] = Array.from({ length: 20 }, (_, rowIndex) => ({
  label: `player ${rowIndex + 1}`,
  data: Array.from({ length: columns.length }, (_, colIndex) => `${colIndex + 1}`)
}))
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
  width: 100vw - 40px;
  display: flex;
  flex-direction: column;
  margin: 0px 20px 20px 20px;
  align-items: center;
}
.game-clock-slider {
  width: 100%;
}

.table-container {
  max-width: 100%;
  color: black;
  overflow: auto;
  border: 1px solid #ccc;
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
