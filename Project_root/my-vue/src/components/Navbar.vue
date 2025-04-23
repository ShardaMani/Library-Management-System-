<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link class="navbar-brand" to="/">Library Management</router-link>
  
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
  
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li v-if="!isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/">Homepage</router-link>
            </li>
            <li v-if="!isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
            <li v-if="!isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/login">User Login</router-link>
            </li>
  
            <li v-if="isAuthenticated && userRole === 'user'" class="nav-item">
              <router-link class="nav-link" to="/user_dashboard">User Dashboard</router-link>
            </li>
            <li v-if="isAuthenticated && userRole === 'librarian'" class="nav-item">
              <router-link class="nav-link" to="/librarian_dashboard">Librarian Dashboard</router-link>
            </li>
            <li v-if="isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/logout">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    computed: {
      isAuthenticated() {
        return this.$store.getters.isAuthenticated;
      },
      userRole() {
        return this.$store.getters.userRole;
      },
    },
  };
  </script>
  
  <style>
  .navbar {
    margin-bottom: 20px;
  }
  </style>
  
  