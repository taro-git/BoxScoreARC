import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import MatchesView from '@/views/MatchesView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/matches',
    name: 'Matches',
    component: MatchesView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
