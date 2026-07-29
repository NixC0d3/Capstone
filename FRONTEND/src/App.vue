<template>
  <BusinessNavBar
    v-if="showNavbar && isBusinessRoute"
  />

  <CharityNavBar
    v-else-if="showNavbar && isCharityRoute"
  />

  <GeneralUserNavBar
    v-else-if="showNavbar && isGeneralUserRoute"
  />

  <AdminNavBar
    v-else-if="showNavbar && isAdminRoute"
  />

  <router-view />
</template>

<script setup>

import { computed } from "vue";
import { useRoute } from "vue-router";

import GeneralUserNavBar from "@/components/Navbar/GeneralUserNavBar.vue";
import BusinessNavBar from "@/components/Navbar/BusinessNavBar.vue";
import CharityNavBar from "@/components/Navbar/CharityNavBar.vue";
import AdminNavBar from "@/components/Navbar/AdminNavBar.vue";

const route = useRoute();

const showNavbar = computed(() =>
  !route.path.startsWith("/login") && !route.path.startsWith("/signup")
);

const isBusinessRoute = computed(() =>
  route.path.startsWith("/business-user")
);

const isCharityRoute = computed(() =>
  route.path.startsWith("/charity-user")
);

const isGeneralUserRoute = computed(() =>
  route.path.startsWith("/generaluser") ||
  route.path.startsWith("/about")
);

const isAdminRoute = computed(() =>
  route.path.startsWith("/admin")
);
</script>