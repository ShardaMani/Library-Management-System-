<template>
    <div class="container mt-5">
      <h2>Manage Requests</h2>
  
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>E-book ID</th>
            <th>Status</th>
            <th>Date Requested</th>
            <th>Grant/Revoke</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.user_id }}</td>
            <td>{{ request.ebook_id }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.date_requested }}</td>
            <td>
              <button
                v-if="request.status === 'pending'"
                @click="grantRequest(request.id)"
                class="btn btn-success btn-sm"
              >
                Grant
              </button>
              <button
                v-if="request.status === 'granted'"
                @click="revokeRequest(request.id)"
                class="btn btn-danger btn-sm"
              >
                Revoke
              </button>
            </td>
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
        requests: [],
      };
    },
    methods: {
        async fetchRequests() {
        console.log('Auth Token:', localStorage.getItem('authToken'));
        try {
            const response = await axios.get('http://127.0.0.1:5000/requests', {
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'),
            },
            });
            this.requests = response.data.requests;
        } catch (error) {
            console.error('Error fetching requests:', error);
        }
        }
        ,
      async grantRequest(id) {
        await axios.post(
          `http://127.0.0.1:5000/requests/${id}/grant`,
          {},
          {
            headers: {
              'Authentication-Token': localStorage.getItem('authToken'),
            },
          }
        );
        this.fetchRequests();
      },
      async revokeRequest(id) {
        await axios.post(
          `http://127.0.0.1:5000/requests/${id}/revoke`,
          {},
          {
            headers: {
              'Authentication-Token': localStorage.getItem('authToken'),
            },
          }
        );
        this.fetchRequests();
      },
    },
    async mounted() {
      this.fetchRequests();
    },
  };
  </script>
  
  <style>
  /* You can add custom styling here */
  </style>
  