<template>
    <div class="teams">
        <div @click="selectedTeam = 'away'" :class="['team', selectedTeam === 'away' ? 'selected' : '']">{{
            boxScoreSummary.away.abbreviation }}</div>
        <div @click="selectedTeam = 'home'" :class="['team', selectedTeam === 'home' ? 'selected' : '']">{{
            boxScoreSummary.home.abbreviation }}</div>
    </div>
    <div class="table-container">
        <table class="fixed-table">
            <thead>
                <tr>
                    <th class="left top-row-1 z-high" :colspan="2">
                        PLAYER
                    </th>
                    <th v-for="(col, colIndex) in columns" :key="'head1-' + colIndex" class="top-row-1">
                        {{ col }}
                    </th>
                </tr>

                <tr>
                    <th class="left top-row-2 z-high" :colspan="2">
                        STARTERS
                    </th>
                    <th class="top-row-2" :colspan="columns.length">
                    </th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="(row, rowIndex) in rows" :key="'row-' + rowIndex">
                    <template v-if="rowIndex === 5">
                        <th class="left top-row-3 z-high" :colspan="2">
                            BENCH
                        </th>
                        <th class="top-row-3" :colspan="columns.length">
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
                            {{ cell }}
                        </td>
                    </template>
                    <template v-else>
                        <th :class="['left1-data', 'inactive']">
                            {{ `#${row.jersey}` }}
                        </th>
                        <th :class="['left2-data', 'inactive']">
                            {{ `${row.player_name} is inactive` }}
                        </th>
                        <th :class="'inactive'" :colspan="columns.length">
                        </th>
                    </template>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import { computed, defineProps, ref, Ref } from 'vue'

import { BOX_SCORE_COLUMNS, BoxScoreData, BoxScoreRow } from '@/types/BoxScore'
import { BoxScoreSummary, Player } from '@/types/BoxScoreSummary';

const props = defineProps<{
    boxScoreSummary: BoxScoreSummary
    boxScoreData: Ref<BoxScoreData>
}>()

const selectedTeam = ref<'home' | 'away'>('away')

const columns = BOX_SCORE_COLUMNS

const convertPlayersToBoxScore = (players: Player[]): BoxScoreRow[] => {
    let boxScoreRows = players.map((player) => ({
        player_id: player.player_id,
        player_name: player.name,
        jersey: player.jersey,
        pos: player.position,
        is_inactive: player.is_inactive,
        comulative_boxscore: props.boxScoreData.value[player.player_id] ?? []
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
    border-spacing: 0px;
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
    background-color: rgb(0, 48, 136);
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
