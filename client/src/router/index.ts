import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import GamesView from '@/views/GamesView.vue'
import GameView from '@/views/GameView.vue'
import TestClickhouse from '@/views/TestClickhouse.vue'
import TestNBAAPI from '@/views/TestNBAAPI.vue'

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
        path: '/news',
        name: 'ClickhouseTest',
        component: TestClickhouse
    },
    {
        path: '/video',
        name: 'NBAAPITest',
        component: TestNBAAPI
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
