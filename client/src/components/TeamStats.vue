<template>
    <v-data-table :headers="headers" :items="teamStats" density="compact" hide-default-footer :items-per-page="-1"
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
import { BOX_SCORE_COLUMNS } from '../types/BoxScore';
import { type TeamStats } from '../types/TeamStats';
import type { GameSummary } from '../types/GameSummary';

const props = defineProps<{
    gameSummary: GameSummary
    teamStats: TeamStats[]
}>()

const headers = computed<DataTableHeader[]>(() => [
    { title: props.gameSummary.awayTeam.abbreviation, align: 'center', sortable: false, key: 'away' },
    { title: '', align: 'center', sortable: false, key: 'boxScoreColumnKey' },
    { title: props.gameSummary.homeTeam.abbreviation, align: 'center', sortable: false, key: 'home' },
])

</script>
