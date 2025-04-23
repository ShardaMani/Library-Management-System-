<template>
  <div class="container mt-5">
    <h1>Welcome to the Library Management System</h1>
    <div class="mt-4">
      <router-link to="/login" class="btn btn-primary mr-2">Login</router-link>
      <router-link to="/register" class="btn btn-secondary">Register</router-link>
    </div>
  </div>
</template>

<script>



export default {
  name: 'Home',
};
</script>

<style scoped>
.container {
  text-align: center;
}
</style>
