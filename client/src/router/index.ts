import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { CLIENT_BASE_URL } from '../appEnv'
import GamesView from '../views/GamesView.vue'
import GameView from '../views/GameView.vue'
import AnalysisView from '../views/AnalysisView.vue'
import HomeView from '../views/HomeView.vue'

export const ROUTE_NAMES = {
    HOME: 'home',
    GAMES: 'games',
    GAME: 'game',
    ANALYSIS: 'analysis',
}

const routes: Array<RouteRecordRaw> = [
    {
        path: `/${ROUTE_NAMES.HOME}`,
        name: ROUTE_NAMES.HOME,
        component: HomeView
    },
    {
        path: `/${ROUTE_NAMES.GAMES}`,
        name: ROUTE_NAMES.GAMES,
        component: GamesView
    },
    {
        path: `/${ROUTE_NAMES.GAME}/:gameId`,
        name: ROUTE_NAMES.GAME,
        component: GameView,
        props: true
    },
    {
        path: `/${ROUTE_NAMES.ANALYSIS}`,
        name: ROUTE_NAMES.ANALYSIS,
        component: AnalysisView
    },
]

const router = createRouter({
    history: createWebHistory(CLIENT_BASE_URL),
    routes
})

export default router
