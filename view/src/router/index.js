import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'upload',
      component: () => import("../views/Upload.vue"),
      meta: {
        title: "Upload Picture",
        requiresAuth: true
      }
    },
    {
      path: '/my',
      name: 'my',
      component: () => import("../views/My.vue"),
      meta: {
        title: "Manage My Image",
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import("../views/Login.vue"),
      meta: {
        title: "Login",
        requiresAuth: false
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import("../views/Register.vue"),
      meta: {
        title: "Register",
        requiresAuth: false
      }
    }
  ]
})

router.beforeEach((to, from) => {
  if (to.meta.title) {
      document.title = to.meta.title + " - MyIMG";
  }
  let token = sessionStorage.getItem('access_token_myimg')
  let local_token = localStorage.getItem("access_token_myimg")
  if (!token && local_token) { 
    sessionStorage.setItem("access_token_myimg", local_token)
    token = local_token
  }
  if (to.meta.requiresAuth && !token) {
      return {
          path: '/login',
      }
  }
})

export default router
