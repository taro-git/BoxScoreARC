<template>
  <v-sheet class="bg-base hide-scroll d-flex flex-column fill-height">
    <v-btn-toggle
      v-model="selectedTeam"
      color="accent"
      class="justify-center"
      mandatory
    >
      <v-col
        v-for="team of Teams"
        :key="team"
        cols="5"
        :class="game.gameSummary.statusId !== 1 ? 'pa-0' : 'px-0'"
      >
        <v-btn :value="team" class="bg-darken w-100">{{
          gameSummary[team].abbreviation
        }}</v-btn>
      </v-col>
    </v-btn-toggle>
    <v-skeleton-loader
      v-if="game.gameSummary.statusId !== 1"
      elevation="7"
      :loading="isLoading"
      color="lighten"
      type="table-row@12"
    >
      <v-responsive class="elevation-7 rounded fill-height">
        <box-score-table
          v-if="!isOccuredError && !isProgressing"
          :game-summary="gameSummary"
          :data="boxScoreTableData"
          :selected-team="selectedTeam"
          :is-collect="boxScore.isCollect"
        />
        <v-empty-state
          v-if="isOccuredError"
          :title="errorMessage"
          class="text-accent"
        />
        <v-progress-circular
          v-if="isProgressing"
          :model-value="progress"
          :rotate="360"
          :size="100"
          :width="15"
          color="accent"
          :style="{
            width: '100%',
            'margin-top': '100px',
            'margin-bottom': '100px',
          }"
        >
          <template v-slot:default> {{ progress }} % </template>
        </v-progress-circular>
      </v-responsive>
    </v-skeleton-loader>
    <v-empty-state v-else title="Comming soon..." :text="gameDatetimeText" />
  </v-sheet>
</template>

<script setup lang="ts">
import { computed, defineProps, onUnmounted, ref, type Ref, watch } from "vue";

import { BoxScoreApi } from "../apis/boxScore.api";
import { GameSummariesApi } from "../apis/gameSummaries.api";
import { ScheduledBoxScoreStatusApi } from "../apis/scheduledBoxScoreStatus.api";
import { updateBoxScoreData } from "../core/boxScoreData";
import { gameStore } from "../store/game";
import {
  BoxScore,
  BoxScoreColumnKeys,
  type BoxScoreTableData,
} from "../types/BoxScore";
import { GameSummary } from "../types/GameSummary";
import BoxScoreTable from "./BoxScoreTable.vue";

const props = defineProps<{
  gameId: string;
  gameClockRange: Ref<number[], number[]>;
}>();

const Teams = {
  AwayTeam: "awayTeam",
  HomeTeam: "homeTeam",
} as const;
// eslint-disable-next-line no-redeclare
type Teams = (typeof Teams)[keyof typeof Teams];
const selectedTeam = ref<Teams>(Teams.AwayTeam);

const isLoading = ref(true);
const isLoaded = ref(true);
const errorMessage = ref("");
const isOccuredError = computed(() => errorMessage.value != "");
const progress = ref<number>(0);
const isProgressing = computed(() => progress.value !== 100);

const game = gameStore();
const gameSummary = game.gameSummary;
const gameDatetimeText = computed(
  () =>
    `scheduled at ${gameSummary.gameDatetime.getFullYear()}/${gameSummary.gameDatetime.getMonth() + 1}/${gameSummary.gameDatetime.getDate()} 
    ${gameSummary.gameDatetime.getHours().toString().padStart(2, "0")}:${gameSummary.gameDatetime.getMinutes().toString().padStart(2, "0")}`,
);

const scheduledBoxScoreStatusApi = new ScheduledBoxScoreStatusApi();
const gameSummariesApi = new GameSummariesApi();
const boxScoreApi = new BoxScoreApi();

const boxScore = ref<BoxScore>(new BoxScore());
const boxScoreTableData = ref<BoxScoreTableData>({});

//
// load init data
// -------------------------------------------------------------------
const getGameData = async () => {
  const gameSummaryResponse = await gameSummariesApi.getGameSummaryByGameId(
    props.gameId,
  );
  gameSummary.awayTeam = gameSummaryResponse[0].awayTeam;
  gameSummary.homeTeam = gameSummaryResponse[0].homeTeam;
  gameSummary.awayPlayers = gameSummaryResponse[0].awayPlayers;
  gameSummary.homePlayers = gameSummaryResponse[0].homePlayers;

  const players = [
    ...gameSummaryResponse[0].homePlayers,
    ...gameSummaryResponse[0].awayPlayers,
  ];
  players.forEach((player) => {
    if (!player.isInactive)
      boxScoreTableData.value[player.playerId] = new Array(
        BoxScoreColumnKeys.length - 1,
      ).fill(0);
  });
  const boxScoreResponse = await boxScoreApi.getBoxScore(props.gameId);
  boxScore.value = boxScoreResponse[0];
  game.finalPeriod = boxScoreResponse[0].finalPeriod;
};

const pollScheduledBoxScoreStatus = async () => {
  try {
    const response =
      await scheduledBoxScoreStatusApi.getScheduledBoxScoreStatus(props.gameId);
    if (!response || Object.keys(response).length === 0) {
      await scheduledBoxScoreStatusApi.postScheduledBoxScoreStatus(
        props.gameId,
      );
    } else if (response[0].errorMessage) {
      throw new Error(response[0].errorMessage);
    } else {
      progress.value = response[0].progress;
      if (progress.value === 100) {
        getGameData().then(() => {
          updateGameData(
            props.gameClockRange.value[0],
            props.gameClockRange.value[1],
          );
        });
        return;
      }
    }
    pollingTimeoutId = setTimeout(pollScheduledBoxScoreStatus, 1000);
  } catch (error) {
    errorMessage.value = String(error);
  } finally {
    isLoading.value = false;
  }
};

let pollingTimeoutId: ReturnType<typeof setTimeout> | null = null;

onUnmounted(() => {
  Object.assign(game.gameSummary, new GameSummary());
  if (pollingTimeoutId) {
    clearTimeout(pollingTimeoutId);
    pollingTimeoutId = null;
  }
});

watch(gameSummary, (gameSummary) => {
  if (isLoaded.value && gameSummary.gameId === props.gameId) {
    isLoaded.value = false;
    isLoading.value = true;
    gameSummary.awayScore = 0;
    gameSummary.homeScore = 0;
    switch (gameSummary.statusId) {
      case 3:
        pollScheduledBoxScoreStatus();
        break;
      case 2:
        getGameData()
          .then(() => {
            updateGameData(0, Number.MAX_SAFE_INTEGER);
            progress.value = 100;
          })
          .catch(() => {
            errorMessage.value = "No data. Updating by 15 minuts.";
          })
          .finally(() => {
            isLoading.value = false;
          });
        break;
      default:
        isLoading.value = false;
    }
  }
});

//
// events
// -------------------------------------------------------------------
const updateGameData = (startRange: number, endRange: number) => {
  const updatedBoxScore = updateBoxScoreData(
    boxScoreTableData.value,
    boxScore.value,
    startRange,
    endRange,
  );
  boxScoreTableData.value = updatedBoxScore.boxScoreTableData;
  game.teamStats = BoxScoreColumnKeys.slice(2).map((key, i) => {
    return {
      boxScoreColumnKey: key,
      home: updatedBoxScore.homeStats[i],
      away: updatedBoxScore.awayStats[i],
    };
  });
  gameSummary.awayScore = gameSummary.awayPlayers
    .filter((player) => !player.isInactive)
    .map((player) => player.playerId)
    .reduce(
      (totalPts, playerId) => totalPts + boxScoreTableData.value[playerId][1],
      0,
    );
  gameSummary.homeScore = gameSummary.homePlayers
    .filter((player) => !player.isInactive)
    .map((player) => player.playerId)
    .reduce(
      (totalPts, playerId) => totalPts + boxScoreTableData.value[playerId][1],
      0,
    );
};
watch(props.gameClockRange, ([startRange, endRange]) => {
  updateGameData(startRange, endRange);
});
</script>

<style scoped></style>
