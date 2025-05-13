import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import MatchesView from '@/views/MatchesView.vue'
import TestView from '@/views/TestView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/matches',
    name: 'Matches',
    component: MatchesView
  },
  {
    path: '/news',
    name: 'ClickhouseTest',
    component: TestView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
