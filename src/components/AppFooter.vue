<!-- Purpose: Reusable footer shown at the bottom of the site. -->
<template>
  <!-- Simple shared footer. -->
      <footer class="mt-5">
          <div class="container">
              <p>Copyright &copy {{ year }} Flask Inc.</p>
          </div>
      </footer>
</template>

<script setup>
// Reusable footer shown at the bottom of the site.
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style>
/* Add any component specific styles here */
</style>