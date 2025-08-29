<template>
    <v-data-table :headers="headers" :items="game.teamStats" density="compact" hide-default-footer :items-per-page="-1"
        class="bg-lighten">
        <template v-slot:item="{ item }">
            <tr class="text-no-wrap text-center">
                <td>{{ item.away }}</td>
                <td class="bg-base">{{ BOX_SCORE_COLUMNS[item.boxScoreColumnKey] }}</td>
                <td>{{ item.home }}</td>
            </tr>
        </template>
    </v-data-table>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { DataTableHeader } from 'vuetify';

import { gameStore } from '../store/game'
import { BOX_SCORE_COLUMNS } from '../types/BoxScore';

const game = gameStore()

const headers = computed<DataTableHeader[]>(() => [
    { title: game.gameSummary.awayTeam.abbreviation, align: 'center', sortable: false, key: 'away' },
    { title: '', align: 'center', sortable: false, key: 'boxScoreColumnKey' },
    { title: game.gameSummary.homeTeam.abbreviation, align: 'center', sortable: false, key: 'home' },
])

</script>
