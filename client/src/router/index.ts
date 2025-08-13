import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { CLIENT_BASE_URL } from '../appEnv'
import GamesView from '../views/GamesView.vue'
import GameView from '../views/GameView.vue'
import AnalysisView from '../views/AnalysisView.vue'
import HomeView from '../views/HomeView.vue'

export const RouteName = {
    Home: 'home',
    Games: 'games',
    Game: 'games/:gameId',
    Analysis: 'analysis',
    Invalid: 'invalid url'
} as const

export type RouteName = (typeof RouteName)[keyof typeof RouteName]

const routes: Array<RouteRecordRaw> = [
    {
        path: `/${RouteName.Home}`,
        name: RouteName.Home,
        component: HomeView
    },
    {
        path: `/${RouteName.Games}`,
        name: RouteName.Games,
        component: GamesView
    },
    {
        path: `/${RouteName.Game}`,
        name: RouteName.Game,
        component: GameView,
        props: true
    },
    {
        path: `/${RouteName.Analysis}`,
        name: RouteName.Analysis,
        component: AnalysisView
    },
]

const router = createRouter({
    history: createWebHistory(CLIENT_BASE_URL),
    routes
})

export default router
