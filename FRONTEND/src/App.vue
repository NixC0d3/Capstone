<template>
  <Navbar v-if="showNavbar" />
  <router-view />
</template>


<script setup>

import { computed } from "vue";
import { useRoute } from "vue-router";

import Navbar from "@/components/Navbar/GeneralUserNavBar.vue";


const route = useRoute();

const showNavbar = computed(() => {
  return route.path !== "/login"
      && route.path !== "/signup";
});

</script>