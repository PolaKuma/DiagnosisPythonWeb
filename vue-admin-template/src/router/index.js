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
    path: '/helloworld',
    name: 'HelloWorld',
    component: () => import('@/views/hello/index'),
    meta: { title: '首页', icon: 'el-icon-s-home' }
  },
  {
    path: '/newsindex',
    name: 'newsIndex',
    component: () => import('@/views/News/index')
  },
  {
    path: '/news',
    name: 'news',
    component: () => import('@/views/News/newsDetail')
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '数据面板', icon: 'dashboard' }
    }]
  },
  {
    path: '/patientManage',
    component: Layout,
    name: 'bookManage',
    meta: { title: '病患管理系统', icon: 'el-icon-s-order' },
    children: [{
      path: 'user',
      name: 'user',
      component: () => import('@/views/patientManage/user.vue'),
      meta: { title: '用户管理', icon: 'el-icon-document' }
    }, {
      path: 'patient',
      name: 'patient',
      component: () => import('@/views/patientManage/patient.vue'),
      meta: { title: '病患管理', icon: 'el-icon-s-claim' }
    }, {
      path: 'diagnosis',
      name: 'diagnosis',
      component: () => import('@/views/patientManage/diagnosis.vue'),
      meta: { title: '检查记录管理', icon: 'el-icon-s-marketing' }
    }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
