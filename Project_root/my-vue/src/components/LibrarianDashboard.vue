<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Librarian Dashboard</h1>

    <!-- Row for Managing Sections and Viewing Requests -->
    <div class="row mb-4">
      <div class="col-md-6 mb-3">
        <button class="btn btn-primary btn-block" @click="navigateToSections">Manage Sections</button>
      </div>
      <div class="col-md-6 mb-3">
        <button class="btn btn-secondary btn-block" @click="navigateToRequests">View Requests</button>
      </div>
    </div>

    <!-- Row for displaying statistics -->
    <div class="row">
      <div class="col-md-6 mb-4">
        <h3>Active Users</h3>
        <canvas id="activeUsersChart"></canvas>
      </div>
      <div class="col-md-6 mb-4">
        <h3>Grant Requests</h3>
        <canvas id="grantRequestsChart"></canvas>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 mb-4">
        <h3>E-books Issued</h3>
        <canvas id="ebooksIssuedChart"></canvas>
      </div>
      <div class="col-md-6 mb-4">
        <h3>E-books Revoked</h3>
        <canvas id="ebooksRevokedChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto';

import axios from "axios";

export default {
  data() {
    return {
      activeUsers: [],
      grantRequests: [],
      ebooksIssued: [],
      ebooksRevoked: [],
    };
  },
  methods: {
    navigateToSections() {
      this.$router.push("/sections");
    },
    navigateToRequests() {
      this.$router.push("/requests");
    },
    fetchData() {
      let token = localStorage.getItem('authToken')
  axios.get("http://127.0.0.1:5000/statistics", {
    headers: {
      "Authentication-Token": `${token}`
    }
  })
  .then((response) => {
    this.activeUsers = response.data.activeUsers;
    this.grantRequests = response.data.grantRequests;
    this.ebooksIssued = response.data.ebooksIssued;
    this.ebooksRevoked = response.data.ebooksRevoked;

    this.renderCharts();
  })
  .catch((error) => {
    console.error("Error fetching statistics:", error);
    // Handle error appropriately, possibly redirect to login if unauthorized
  });
}
,
    renderCharts() {
      new Chart(document.getElementById("activeUsersChart"), {
        type: "bar",
        data: {
          labels: ["Active Users"],
          datasets: [
            {
              label: "Active Users",
              data: [this.activeUsers],
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        },
      });

      new Chart(document.getElementById("grantRequestsChart"), {
        type: "bar",
        data: {
          labels: ["Grant Requests"],
          datasets: [
            {
              label: "Grant Requests",
              data: [this.grantRequests],
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
          ],
        },
      });

      new Chart(document.getElementById("ebooksIssuedChart"), {
        type: "bar",
        data: {
          labels: ["E-books Issued"],
          datasets: [
            {
              label: "E-books Issued",
              data: [this.ebooksIssued],
              backgroundColor: "rgba(153, 102, 255, 0.2)",
              borderColor: "rgba(153, 102, 255, 1)",
              borderWidth: 1,
            },
          ],
        },
      });

      new Chart(document.getElementById("ebooksRevokedChart"), {
        type: "bar",
        data: {
          labels: ["E-books Revoked"],
          datasets: [
            {
              label: "E-books Revoked",
              data: [this.ebooksRevoked],
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
            },
          ],
        },
      });
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
h1 {
  font-size: 2.5rem;
}
canvas {
  width: 100% !important;
  height: 300px !important;
}
</style>
