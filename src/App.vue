<!-- Purpose: Root Vue layout. It displays the shared header, the active page from the router, and the footer. -->
<script setup>
// Root Vue layout. It displays the shared header, the active page from the router, and the footer.
// AppHeader and AppFooter stay visible on every page.
// RouterView is where Vue Router displays the currently selected view.
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <!-- Shared layout: header at the top, active route in the middle, footer at the bottom. -->
  <AppHeader />

  <main>
    <RouterView />
  </main>
  
  <AppFooter />
</template>

<style>
body {
  padding-top: 75px;
}
</style>