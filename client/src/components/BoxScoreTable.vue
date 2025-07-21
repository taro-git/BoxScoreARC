<template>
    <v-sheet class="table-container bg-base fill-height" fluid>
        <table class="fixed-table">
            <thead>
                <tr>
                    <th class="left top-row-1 z-high bg-darken" :colspan="2">
                        PLAYER
                    </th>
                    <th v-for="(col, colIndex) in BOX_SCORE_COLUMN_KEYS" :key="'head1-' + colIndex"
                        class="top-row-1 bg-darken">
                        {{ BOX_SCORE_COLUMNS[col] }}
                    </th>
                </tr>

                <tr>
                    <th class="left top-row-2 z-high" :colspan="2">
                        STARTERS
                    </th>
                    <th class="top-row-2" :colspan="BOX_SCORE_COLUMN_KEYS.length">
                    </th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="(row, rowIndex) in rows" :key="'row-' + rowIndex">
                    <template v-if="rowIndex === 5">
                        <th class="left top-row-3 z-high" :colspan="2">
                            BENCH
                        </th>
                        <th class="top-row-3" :colspan="BOX_SCORE_COLUMN_KEYS.length">
                        </th>
                    </template>
                    <template v-else-if="!row.is_inactive">
                        <th :class="['left1-data', [rowIndex % 2 !== 0 ? 'odd-row' : '']]">
                            {{ `#${row.jersey}` }}
                        </th>
                        <th :class="['left2-data', [rowIndex % 2 !== 0 ? 'odd-row' : '']]">
                            {{ row.player_name }}
                        </th>

                        <td :class="['data', [rowIndex % 2 !== 0 ? 'odd-row' : '']]">
                            {{ row.pos }}
                        </td>
                        <td :class="['data', [rowIndex % 2 !== 0 ? 'odd-row' : '']]"
                            v-for="(cell, colIndex) in row.comulative_boxscore"
                            :key="'cell-' + rowIndex + '-' + colIndex">
                            <template v-if="colIndex == 8 || colIndex == 11 || colIndex == 14">
                                {{ `${cell}%` }}
                            </template>
                            <template v-else>
                                {{ cell }}
                            </template>
                        </td>
                    </template>
                    <template v-else>
                        <th :class="['left1-data', 'inactive']">
                            {{ `#${row.jersey}` }}
                        </th>
                        <th :class="['left2-data', 'inactive']">
                            {{ `${row.player_name} is inactive` }}
                        </th>
                        <th :class="'inactive'" :colspan="BOX_SCORE_COLUMN_KEYS.length">
                        </th>
                    </template>
                </tr>
            </tbody>
        </table>
    </v-sheet>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { BOX_SCORE_COLUMN_KEYS, BOX_SCORE_COLUMNS, type BoxScoreData, type BoxScoreRow } from '../types/BoxScore'
import { type BoxScoreSummary, type Player } from '../types/BoxScoreSummary';

const props = defineProps<{
    boxScoreSummary: BoxScoreSummary
    boxScoreData: BoxScoreData
    selectedTeam: string
    gameClockRange: number[]
}>()

const convertPlayersToBoxScore = (players: Player[]): BoxScoreRow[] => {
    let boxScoreRows = players.map((player) => ({
        player_id: player.player_id,
        player_name: player.name,
        jersey: player.jersey,
        pos: player.position,
        is_inactive: player.is_inactive,
        comulative_boxscore: props.boxScoreData[player.player_id] ?? []
    }))
    boxScoreRows.splice(5, 0, {
        player_id: 0,
        player_name: 'no data',
        jersey: '',
        pos: '',
        is_inactive: false,
        comulative_boxscore: []
    })
    return boxScoreRows
}

const boxScore = computed(() => ({
    home: convertPlayersToBoxScore(props.boxScoreSummary.home.players),
    away: convertPlayersToBoxScore(props.boxScoreSummary.away.players)
}))

const rows = computed(() => {
    return props.selectedTeam === 'home' ? boxScore.value.home : boxScore.value.away
})

</script>

<style scoped>
.table-container {
    max-width: 100%;
    overflow: auto;
    border: 1px solid #ccc;
}

.fixed-table {
    border-spacing: 0px;
    color: #000;
}

.fixed-table th,
.fixed-table td {
    padding: 6px 10px;
    white-space: nowrap;
}

.top-row-1 {
    position: sticky;
    top: 0;
    z-index: 2;
    padding: 0 !important;
    height: 20px;
    box-sizing: border-box;
    color: white;
    font-size: 10px;
    text-align: center;
}

.top-row-2 {
    position: sticky;
    top: 20px;
    z-index: 2;
    padding: 0 !important;
    height: 15px;
    box-sizing: border-box;
    font-size: 10px;
    text-align: center;
    background-color: #999999;
}

.top-row-3 {
    position: sticky;
    top: 35px;
    padding: 0 !important;
    height: 15px;
    box-sizing: border-box;
    font-size: 10px;
    text-align: center;
    background-color: #999999;
}

.z-high {
    z-index: 3;
}

.left {
    position: sticky;
    left: 0;
}

.left1-data {
    position: sticky;
    left: 0;
    max-width: 46px;
    min-width: 46px;
    font-size: 14px;
    box-sizing: border-box;
    background-color: white;
    text-align: left;
}

.left2-data {
    position: sticky;
    left: 46px;
    background-color: white;
    text-align: left;
    border-right: 1px solid #999999;
}

.data {
    z-index: 1;
    text-align: center;
    background-color: white;
}

.odd-row {
    background-color: #f1f1f1;
}

.inactive {
    background-color: #999999;
    text-align: left;
    overflow: visible;
    max-width: 0px;
}
</style>
