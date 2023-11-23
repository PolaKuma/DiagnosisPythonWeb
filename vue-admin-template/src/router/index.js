import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/icon.vue'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/chathome',
    component: Home,
    children: [{
      path: '/chatHome',
      name: 'chatHome',
      component: () => import('@/views/pages/chatHome/index')
    }]
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    name: 'HelloWorld',
    redirect: '/helloworld',
    component: () => import('@/views/hello/index'),
    meta: { title: 'Index', icon: 'el-icon-s-order' }
  },
  {
    path: '/dashboard',
    component: Layout,
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: {title: 'Dashboard', icon: 'dashboard'}
    }]
  },
  {
    path: '/patientManage',
    component: Layout,
    name: 'bookManage',
    meta: {title: '病患管理系统', icon: 'el-icon-s-order'},
    children: [{
      path: 'user',
      name: 'user',
      component: () => import('@/views/patientManage/user.vue'),
      meta: {title: '用户管理', icon: 'el-icon-document'}
    }, {
      path: 'book',
      name: 'book',
      component: () => import('@/views/patientManage/patient.vue'),
      meta: {title: '病患管理', icon: 'el-icon-goods'}
    }, {
      path: 'read',
      name: 'read',
      component: () => import('@/views/patientManage/diagnosis.vue'),
      meta: {title: '检查记录管理', icon: 'el-icon-goods'}
    }
    ]
  },

  // 404 page must be placed at the end !!!
  {path: '*', redirect: '/404', hidden: true}
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({y: 0}),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
