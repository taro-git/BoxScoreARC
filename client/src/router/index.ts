import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import GamesView from '@/views/GamesView.vue'
import GameView from '@/views/GameView.vue'
import AnalysysView from '@/views/AnalysysView.vue'
import DataView from '@/views/DataView.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/games',
        name: 'games',
        component: GamesView
    },
    {
        path: '/games/:gameDate/:gameId',
        name: 'game',
        component: GameView,
        props: true
    },
    {
        path: '/analysys',
        name: 'analysys',
        component: AnalysysView
    },
    {
        path: '/data',
        name: 'data',
        component: DataView
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
