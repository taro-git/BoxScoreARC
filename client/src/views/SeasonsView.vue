<template>
  <v-select label="Season" :items="seasons" v-model="season" />
  <v-radio-group v-model="tableSeparation" inline>
    <v-radio label="All" value="all" />
    <v-radio label="Conference" value="conferences" />
    <v-radio label="Division" value="divisions" />
  </v-radio-group>
  <v-data-table
    v-for="segment in tableSeparation == 'all'
      ? ['']
      : tableSeparation == 'conferences'
        ? conferences
        : divisions"
    :key="segment"
    :headers="headers"
    :items="
      tableSeparation == 'all'
        ? regularSeasonTeamStats
        : regularSeasonTeamStats.filter(
            (item) => item.conference == segment || item.division == segment,
          )
    "
    density="compact"
    :sort-by="
      tableSeparation == 'all'
        ? [
            { key: 'pct', order: 'desc' },
            { key: 'conferenceRank', order: 'asc' },
          ]
        : [{ key: 'conferenceRank', order: 'asc' }]
    "
    hide-default-footer
    :items-per-page="-1"
    class="bg-lighten mb-2"
  >
    <template v-slot:top>
      <v-toolbar-title class="pl-5 bg-darken">
        {{ segment }}
      </v-toolbar-title>
    </template>
    <template v-slot:[`item.team`]="{ item }">
      <div
        style="display: inline-flex; align-items: center; white-space: nowrap"
      >
        <img :src="item.teamLogo" alt="logo" width="30" height="30" />
        <span style="margin-left: 6px">{{ item.teamAbbreviation }}</span>
      </div>
    </template>
  </v-data-table>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { DataTableHeader } from "vuetify";

import { SeasonSummariesApi } from "../apis/seasonSummaries.api";
import {
  conferences,
  divisions,
  type RegularSeasonTeamStats,
  SeasonSummary,
} from "../types/SeasonSummary";

const seasonSummariesApi = new SeasonSummariesApi();
const seasonSummaries = ref<SeasonSummary[]>([]);
const seasons = ref<string[]>();
const season = ref<string>();
const tableSeparation = ref("conferences");
const regularSeasonTeamStats = computed<RegularSeasonTeamStats[]>(
  () =>
    seasonSummaries.value.filter((item) => item.season == season.value)[0]
      ?.teams ?? [],
);
const headers: DataTableHeader[] = [
  { title: "Rank", align: "center", sortable: true, key: "conferenceRank" },
  { title: "Team", align: "center", sortable: true, key: "team" },
  { title: "Win", align: "center", sortable: true, key: "win" },
  { title: "Lose", align: "center", sortable: true, key: "lose" },
  { title: "GB", align: "center", sortable: true, key: "gb" },
  { title: "PCT", align: "center", sortable: true, key: "pct" },
];

//
// load init data
// -------------------------------------------------------------------
seasonSummariesApi.getSeasonSummaries().then((response) => {
  seasonSummaries.value = response.sort((a, b) =>
    b.season.localeCompare(a.season),
  );
  seasons.value = seasonSummaries.value.map(
    (seasonSummary) => seasonSummary.season,
  );
  season.value = seasonSummaries.value[0].season;
});
</script>
