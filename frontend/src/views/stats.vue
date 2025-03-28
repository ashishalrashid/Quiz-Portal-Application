<template>
    <div class="container">
      <div class="admin-dashboard">
        <RouterLink to="/admindash" class="icon">
          <i class="fas fa-home"> Home</i>
        </RouterLink>
        <RouterLink to="/admindash/subjects" class="icon">
          <i class="fas fa-book circular-icon"> Subjects</i>
        </RouterLink>
        <RouterLink to="/admindash/user" class="icon">
          <i class="fas fa-user circular-icon"> Users</i>
        </RouterLink>
        <RouterLink to="/admindash/stats" class="disabled">
          <i class="fas fa-chart-bar"> Stats</i>
        </RouterLink>
        <a href="#" @click.prevent="logout" class="icon">
          <i class="fas fa-sign-out-alt"> Log Out</i>
        </a>
      </div>
      <div class="main-content">
        <h2>Subject Statistics</h2>
        <canvas id="subjectChart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);
  export default {
    name: "SubjectStats",
    data() {
      return {
        stats: []
      };
    },
    async created() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5000/subjectstats", {
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + token
          }
        });
        const data = await response.json();
        this.stats = data.stats;
        this.renderChart();
      } catch (error) {
        console.error("Error fetching subject statistics:", error);
      }
    },
    methods: {
      renderChart() {
        const ctx = document.getElementById("subjectChart").getContext("2d");
        const labels = this.stats.map(stat => stat.name);
        const userCounts = this.stats.map(stat => stat.user_count);
        const avgScores = this.stats.map(stat => stat.avg_score ? parseFloat(stat.avg_score) : 0);
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: "User Count",
                data: userCounts,
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1
              },
              {
                label: "Average Score",
                data: avgScores,
                backgroundColor: "rgba(153, 102, 255, 0.2)",
                borderColor: "rgba(153, 102, 255, 1)",
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      },
      logout() {
        localStorage.removeItem("token");
        this.$router.push("/login");
      }
    }
  };
  </script>
  
  <style>
  html, body, #app {
    margin: 0;
    width: 100%;
  }
  .container {
    font-family: 'Times New Roman', Times, serif;
    display: flex;
    background-color: rgb(213, 213, 213);
    width: 100%;
  }
  .admin-dashboard {
    background-color: rgb(56, 56, 56);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 10px;
    align-items: flex-start;
    width: 250px;
  }
  .icon {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 10px;
    border-radius: 250px;
    margin: 10px;
    color: white;
    width: 80%;
    font-family: 'Times New Roman', Times, serif;
  }
  .icon:hover {
    background-color: #000000;
    transform: scale(1.1);
  }
  .disabled {
    background-color: rgb(117, 116, 116);
    padding: 10px;
    border-radius: 250px;
    margin: 10px;
    width: 80%;
    color: aliceblue;
  }
  .main-content {
    flex-grow: 1;
    padding: 20px;
  }
  </style>
  