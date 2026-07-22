import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue")
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue")
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue")
    },
    {
      path: "/explore",
      name: "explore",
      component: () => import("../views/ExploreView.vue")
    },
    {
      path: "/organisations/:id",
      name: "organisation-details",
      component: () => import("../views/OrganisationDetailsView.vue")
    },
    {
      path: "/recommendations",
      name: "recommendations",
      component: () => import("../views/RecommendationsView.vue")
    },
    {
      path: "/saved",
      name: "saved-organisations",
      component: () => import("../views/SavedOrganisationsView.vue")
    },
    {
      path: "/volunteers",
      name: "volunteers",
      component: () => import("../views/VolunteerOpportunitiesView.vue")
    },
    {
      path: "/messages",
      name: "messages",
      component: () => import("../views/MessagesView.vue")
    },
    {
      path: "/user-dashboard",
      name: "user-dashboard",
      component: () => import("../views/UserDashboardView.vue")
    },
    {
      path: "/organisation-dashboard",
      name: "organisation-dashboard",
      component: () => import("../views/OrganisationDashboardView.vue")
    },
    {
      path: "/admin",
      name: "admin-dashboard",
      component: () => import("../views/AdminDashboardView.vue")
    },
    {
      path: "/reports",
      name: "monthly-report",
      component: () => import("../views/MonthlyReportView.vue")
    }
  ]
});

export default router;
