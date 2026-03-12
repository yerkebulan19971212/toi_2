import { createRouter, createWebHistory } from 'vue-router'
import EventDashboardPage from './components/EventDashboardPage.vue'
import InvitationPage from './components/InvitationPage.vue'
import LandingPage from './components/LandingPage.vue'
import TemplatesPage from './components/TemplatesPage.vue'
import WeddingTemplate01 from './components/WeddingTemplate01.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: LandingPage,
  },
  {
    path: '/templates',
    name: 'templates',
    component: TemplatesPage,
  },
  {
    path: '/event/:slug',
    name: 'event-dashboard',
    component: EventDashboardPage,
    props: true,
  },
  {
    path: '/invite/:slug?',
    name: 'invitation',
    component: InvitationPage,
    props: route => ({ slug: route.params.slug || 'ayan-aruzhan' }),
  },
  {
    path: '/wedding-template-01',
    name: 'wedding-template-01',
    component: WeddingTemplate01,
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

