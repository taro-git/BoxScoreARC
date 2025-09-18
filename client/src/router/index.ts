import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";

import { CLIENT_BASE_URL } from "../appEnv";
import AnalysisView from "../views/AnalysisView.vue";
import GamesView from "../views/GamesView.vue";
import GameView from "../views/GameView.vue";
import LicensesView from "../views/LicensesView.vue";
import SeasonsView from "../views/SeasonsView.vue";

export const RouteName = {
  Seasons: "seasons",
  Games: "games",
  Game: "games/:gameId",
  Analysis: "analysis",
  Licenses: "licenses",
  Invalid: "invalid url",
} as const;

export type RouteName = (typeof RouteName)[keyof typeof RouteName];

const routes: Array<RouteRecordRaw> = [
  {
    path: `/${RouteName.Seasons}`,
    name: RouteName.Seasons,
    component: SeasonsView,
  },
  {
    path: `/${RouteName.Games}`,
    name: RouteName.Games,
    component: GamesView,
  },
  {
    path: `/${RouteName.Game}`,
    name: RouteName.Game,
    component: GameView,
    props: true,
  },
  {
    path: `/${RouteName.Analysis}`,
    name: RouteName.Analysis,
    component: AnalysisView,
  },
  {
    path: `/${RouteName.Licenses}`,
    name: RouteName.Licenses,
    component: LicensesView,
  },
];

const router = createRouter({
  history: createWebHistory(CLIENT_BASE_URL),
  routes,
});

export default router;
