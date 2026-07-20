<!-- Purpose: Page-level registration screen placeholder for the Vue frontend. -->
<template>
  <!-- Basic placeholder registration form for the Vue version of the app. -->
  <div class="container">
    <h1>Create Account</h1>
    <p class="text-muted">Register as a general user, business user, charity user, or admin.</p>

    <form class="card card-body">
      <div class="row">
        <div class="col-md-6">
          <label class="form-label">First Name</label>
          <input class="form-control mb-3" />
        </div>

        <div class="col-md-6">
          <label class="form-label">Last Name</label>
          <input class="form-control mb-3" />
        </div>
      </div>

      <label class="form-label">Email</label>
      <input class="form-control mb-3" type="email" />

      <label class="form-label">Account Type</label>
      <select class="form-select mb-3">
        <option>General User</option>
        <option>Business User</option>
        <option>Charity User</option>
      </select>

      <button class="btn btn-primary">Register</button>
    </form>
  </div>
</template>
