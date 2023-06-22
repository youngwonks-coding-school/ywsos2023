import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("../views/ProfileView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue"),
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: () => import("../views/DashboardView.vue"),
    },
    {
      path: "/logout",
      name: 'logout',
      redirect: to => {
        console.log({
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
          }
        })
        axios.post('/api/auth/logout', {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('accessToken')}`
            }
          }).then((response) => {
            console.log('successfuly logged out.')
            localStorage.removeItem('refreshToken')
            localStorage.removeItem('accessToken')
          }).catch((error) => {
            console.log('error', error)
          })

        return 'login'
      },
    }

  ],
});

export default router;
