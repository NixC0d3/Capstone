import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({

  history: createWebHistory(),

  routes: [
    {
      path: "/",
      redirect: "/login"
    },
    {
      path: "/login",
      component: () => import("@/views/auth/LoginView.vue")
    },

    {
      path: "/signup",
      component: () => import("@/views/auth/Signup.vue")
    },
    {
      path: "/generaluser/home",
      component: () => import("@/views/general-user/GeneralUserHome.vue")
    },
    {
      path: "/organisation/:id",
      component: () => import("@/views/general-user/OrgView.vue")
    },

    {
      path: "/generaluser/charities",
      component: () => import("@/views/general-user/GeneralUserCharity.vue")
    },
    {
      path: "/generaluser/volunteer-opportunities",
      component: () => import("@/views/general-user/VolunteerOpportunities.vue")
    },
    
    {
      path: "/generaluser/profile",
      component: () => import("@/views/general-user/GeneralUserProfile.vue")
    },
    {
      path: "/generaluser/inbox",
      component: () => import("@/views/Inbox.vue")
    },
    {
      path: "/business-user/inbox",
      component: () => import("@/views/Inbox.vue")
    },
    {
      path: "/charity-user/inbox",
      component: () => import("@/views/Inbox.vue")
    },
    {
      path: "/business-user/home",
      component: () => import("@/views/business-owner/BusinessHome.vue")
    },
    {
      path: "/charity-user/home",
      component: () => import("@/views/charity-owner/CharityHome.vue")
    },
    {
      path: "/about",
      component: () => import("@/views/About.vue")
    },
    {
      path: "/business-user/profile",
      component: () => import("@/views/business-owner/BusinessProfile.vue")
    },
    {
      path: "/charity-user/profile",
      component: () => import("@/views/charity-owner/CharityProfile.vue")
    },
    
    {
      path: "/business-user/create-organisation",
      component: () => import("@/views/business-charity/CreateOrg.vue"),
      props: {
        organisationType: "business"
      }
    },
    {
      path: "/charity-user/create-organisation",
      component: () => import("@/views/business-charity/CreateOrg.vue"),
      props: {
        organisationType: "charity"
      }
    },
    {
      path: "/business-user/edit-organisation",
      component: () => import("@/views/business-charity/EditOrg.vue"),
      props: {
        organisationType: "business"
      }
    },
    {
      path: "/charity-user/edit-organisation",
      component: () => import("@/views/business-charity/EditOrg.vue"),
      props: {
        organisationType: "charity"
      }
    },
    {
      path: "/charity-user/volunteer-matches",
      name: "CharityVolunteerMatches",
      component: () => import("@/views/charity-owner/VolunteerMatches.vue")
    },
    {
      path: "/admin/home",
      component: () => import("@/views/admin/AdminHome.vue")

    },
    {
      path: "/admin/users",
      component: () => import("@/views/admin/AdminUsers.vue")
    },
    {
      path: "/admin/settings",
      component: () => import("@/views/admin/AdminSettings.vue")
    },
    {
      path:"/admin/users/:id",
      component: () => import("@/views/admin/AdminUserDetails.vue")
    },
    {
      path:"/admin/organisations",
      component: () => import("@/views/admin/AdminOrganisations.vue")
    },
    {
      path: "/admin/organisations/:id",
      component: () => import("@/views/admin/AdminOrgDetails.vue")
    }

  ]
});


export default router;
