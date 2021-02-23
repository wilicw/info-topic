import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/teachers', component: () => import('../views/Teachers.vue') },
  { path: '/teachers/:id', component: () => import('../views/Teachers_topics.vue') },
  { path: '/search', component: () => import('../views/Search.vue') },
  { path: '/search/:word', component: () => import('../views/Search_topics.vue') },
  { path: '/topic/:uuid', component: () => import('../views/Detail.vue') },
  { path: '/keyword/:word', component: () => import('../views/Keyword.vue') },
  { path: '/edit/:id', component: () => import('../views/Edit.vue') },
  { path: '/menu', component: () => import('../views/Menu.vue') },
  { path: '/logout', component: () => import('../views/Logout.vue') },
  { path: '/change_password', component: () => import('../views/Change_password.vue') },
  { path: '/change_weight', component: () => import('../views/Change_weight.vue') },
  { path: '/score', component: () => import('../views/Score.vue') }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
