import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import MatchesView from '@/views/MatchesView.vue'
import TestClickhouse from '@/views/TestClickhouse.vue'
import TestNBAAPI from '@/views/TestNBAAPI.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/matches',
    name: 'Matches',
    component: MatchesView
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
