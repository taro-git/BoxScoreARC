<template>
    <v-sheet class="bg-base">
        <v-container v-for="gameSummary in gameSummaries">
            <v-skeleton-loader elevation="7" :loading="isLoading" type="image" class="w-100" color="lighten">
                <v-responsive class="elevation-7 rounded">
                    <GameCard :game-summary="gameSummary" :score-display="true" :full-view="true"
                        :game-date-display="true" :disableLink="game.gameSummary.gameId == gameSummary.gameId" />
                </v-responsive>
            </v-skeleton-loader>
        </v-container>
        <v-card v-if="gameSummaries.length === 0 && !isError && !isLoading" elevation="0" class="bg-base">
            <v-card-title class="text-center text-h3 justify-center">no game</v-card-title>
        </v-card>
        <v-empty-state v-if="isError" title="Whoops, Server Error" :text="errorMessage" class="text-accent" />
    </v-sheet>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

import { GameSummariesApi } from '../apis/gameSummaries.api';
import GameCard from '../components/GameCard.vue';
import { gameStore } from '../store/game';
import { GameSummary } from '../types/GameSummary';

const isLoading = ref(true)
const game = gameStore()
const gameSummaries = ref<GameSummary[]>([])
const errorMessage = ref('')
const isError = computed<boolean>(() => errorMessage.value != '')

new GameSummariesApi().getGameSummaryByMatchUp([game.gameSummary.awayTeam.teamId, game.gameSummary.homeTeam.teamId]).then((response) => {
    gameSummaries.value = response.sort((a, b) => b.gameDatetime.getTime() - a.gameDatetime.getTime())
}).catch(
    e => errorMessage.value = e
).finally(
    () => isLoading.value = false
)
</script>
