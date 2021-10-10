import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: () => import('../views/Public/Home.vue') },
  { path: '/login', component: () => import('../views/Public/Login.vue') },
  { path: '/teachers', component: () => import('../views/Public/Teachers.vue') },
  { path: '/teachers/:id', component: () => import('../views/Public/Teachers_topics.vue') },
  { path: '/search', component: () => import('../views/Public/Search.vue') },
  { path: '/search/:word', component: () => import('../views/Public/Search_topics.vue') },
  { path: '/topic/:uuid', component: () => import('../views/Public/Detail.vue') },
  { path: '/keyword/:word', component: () => import('../views/Public/Keyword.vue') },
  { path: '/edit/:id', component: () => import('../views/Manager/Edit.vue') },
  { path: '/menu', component: () => import('../views/Manager/Menu.vue') },
  { path: '/logout', component: () => import('../views/Public/Logout.vue') },
  { path: '/change_password', component: () => import('../views/Manager/Change_password.vue') },
  { path: '/change_weight', component: () => import('../views/Manager/Teacher/Change_weight.vue') },
  { path: '/new', component: () => import('../views/Manager/Student/New_topic.vue') },
  { path: '/edit_topics', component: () => import('../views/Manager/Teacher/All_topics.vue') },
  { path: '/score', component: () => import('../views/Manager/Teacher/Score.vue') },
  { path: '/export_score', component: () => import('../views/Manager/Teacher/Export_score.vue') },
  { path: '/import', component: () => import('../views/Manager/Teacher/Import_score.vue') },
  { path: '/reference', component: () => import('../views/Public/Reference.vue') },
  { path: '/year/:y', component: () => import('../views/Public/Year_topics.vue') },
  { path: '/rank/:y', component: () => import('../views/Public/Rank_topics.vue') },
  { path: '/import_student', component: () => import('../views/Manager/Teacher/Import_students.vue') },
  { path: '/change_teachers', component: () => import('../views/Manager/Teacher/Change_teachers.vue') },
  { path: '/year/latest', component: () => import('../views/Public/Year_topics.vue') },
  { path: '/:path(.*)', component: () => import('../views/Public/Not_found.vue') },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
