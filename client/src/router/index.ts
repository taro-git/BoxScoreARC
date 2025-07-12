import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import GamesView from '@/views/GamesView.vue'
import GameView from '@/views/GameView.vue'
import AnalysysView from '@/views/AnalysysView.vue'
import SettingsView from '@/views/SettingsView.vue'

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
        path: '/settings',
        name: 'settings',
        component: SettingsView
    }
]

const router = createRouter({
    history: createWebHistory(process.env.VUE_APP_CLIENT_BASE_URL),
    routes
})

export default router
