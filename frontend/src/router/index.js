import { createRouter, createWebHistory } from 'vue-router'
import SalesOverview from '../views/SalesOverview.vue'
import TopProducts from '../views/TopProducts.vue'
import SalesBreakdown from '../views/SalesBreakdown.vue'
import TicketTrend from '../views/TicketTrend.vue'
import OperationalTime from '../views/OperationalTime.vue'
import CustomerRetention from '../views/CustomerRetention.vue'

const routes = [
  {
    path: '/',
    name: 'SalesOverview',
    component: SalesOverview
  },
  {
    path: '/top-products',
    name: 'TopProducts',
    component: TopProducts
  },
  {
    path: '/sales-breakdown',
    name: 'SalesBreakdown',
    component: SalesBreakdown
  },
  {
    path: '/ticket-trend',
    name: 'TicketTrend',
    component: TicketTrend
  },
  {
    path: '/operational-time',
    name: 'OperationalTime',
    component: OperationalTime
  },
  {
    path: '/customer-retention',
    name: 'CustomerRetention',
    component: CustomerRetention
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
