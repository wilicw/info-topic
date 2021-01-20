import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Teachers from '../views/Teachers.vue'
import Search from '../views/Search.vue'
import Detail from '../views/Detail.vue'
import Edit from '../views/Edit.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component:Teachers
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/view/:id',
    name: 'Detail',
    component: Detail
  },
  {
    path: '/edit/:id',
    name: 'Edit',
    component: Edit
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
