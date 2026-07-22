<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/">CivilInfoHub</RouterLink>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link">Home</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/explore" class="nav-link">Explore</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/recommendations" class="nav-link">Recommendations</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/volunteers" class="nav-link">Volunteers</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/messages" class="nav-link">Messages</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/reports" class="nav-link">Reports</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/admin" class="nav-link">Admin</RouterLink>
            </li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink to="/login" class="nav-link">Login</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/register" class="nav-link">Register</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
