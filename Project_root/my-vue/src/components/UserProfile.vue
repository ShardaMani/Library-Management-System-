<template>
  <div class="container mt-5">
    <h2>User Profile</h2>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ profile.email }}</h5>
        <p class="card-text">
          <strong>Active: </strong> {{ profile.active ? 'Yes' : 'No' }}
        </p>
        <p class="card-text">
          <strong>Roles: </strong> {{ profile.roles.join(', ') }}
        </p>
      </div>
    </div>
    <hr />
    <h3>Active Requests</h3>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Ebook ID</th>
          <th>Ebook Name</th>
          <th>Date of Request</th>
          <th>Date of Return</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in activeRequests" :key="request.ebook_id">
          <td>{{ request.ebook_id }}</td>
          <td>{{ request.ebook_name }}</td>
          <td>{{ request.date_of_request }}</td>
          <td>{{ request.date_of_return }}</td>
          <td>{{ request.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      profile: {
        email: '',
        active: false,
        roles: [],
      },
      activeRequests: []
    };
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/user_details', {
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('authToken'),
          },
        });
        this.profile = response.data.user;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async fetchActiveRequests() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/active_requests', {
          headers: {
            'Authentication-Token': localStorage.getItem('authToken'),
          },
        });
        this.activeRequests = response.data.active_requests;
        console.log(this.activeRequests);
        console.log(response.data.active_requests);
      } catch (error) {
        console.error('Error fetching active requests:', error);
      }
    }
  },
  mounted() {
    this.fetchUserProfile();
    this.fetchActiveRequests();
  },
};
</script>

<style>
/* Add custom styles here if needed */
</style>
