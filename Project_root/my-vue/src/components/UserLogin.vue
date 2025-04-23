<template>
  <div class="container mt-5">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email</label>
        <input 
          id="email"
          type="email" 
          v-model.trim="email" 
          class="form-control" 
          required 
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input 
          id="password"
          type="password" 
          v-model.trim="password" 
          class="form-control" 
          required 
        />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="isLoading">
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
    <div v-if="error" class="alert alert-danger mt-3">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: '',
      isLoading: false,
      error: null,
    };
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const credentials = {
          email: this.email,
          password: this.password,
        };
        const { role } = await this.login(credentials);

        // Redirect based on role
        if (role.includes('admin')) {
          this.$router.push('/librarian_dashboard');
        } else {
          this.$router.push('/user_dashboard');
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'An error occurred during login';
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
</style>