import { createRouter, createWebHistory } from "vue-router";

import LoginView from "@/views/auth/LoginView.vue";
import Signup from "@/views/auth/Signup.vue";
import About from "@/views/About.vue";

import GeneralUserHome from "@/views/general-user/GeneralUserHome.vue";
import GeneralUserProfile from "@/views/general-user/GeneralUserProfile.vue";
import GeneralUserCharity from "@/views/general-user/GeneralUserCharity.vue";

import OrgView from "@/views/general-user/OrgView.vue";
import Inbox from "@/views/Inbox.vue";
const router = createRouter({

  history: createWebHistory(),

  routes: [
    {
      path: "/",
      redirect: "/login"
    },
    {
      path: "/login",
      component: LoginView
    },

    {
      path: "/signup",
      component: Signup
    },
    {
      path: "/generaluser/home",
      component: GeneralUserHome
    },
    {
      path: "/organisation/:id",
      component: OrgView
    },

    {
      path: "/generaluser/charities",
      component: GeneralUserCharity
    },
    {
      path: "/generaluser/profile",
      component: GeneralUserProfile
    },
    {
      path: "/generaluser/inbox",
      component: Inbox
    },
    {
      path: "/about",
      component: About
    }

    
  ]
});


export default router;