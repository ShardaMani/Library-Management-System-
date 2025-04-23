<template>
  <div class="container mt-5">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" v-model="username" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" v-model="email" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" v-model="password" class="form-control" required />
      </div>
      
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
    };
  },
  methods: {
    register() {
      const user = {
        username: this.username,
        email: this.email,
        password: this.password,
      };
      axios.post('http://127.0.0.1:5000/register', user)
        .then(() => {
          alert('Registration successful!');
          this.$router.push('/login');
        })
        .catch(err => {
          alert('Registration failed: ' + err.response.data.message);
        });
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
}
</style>
