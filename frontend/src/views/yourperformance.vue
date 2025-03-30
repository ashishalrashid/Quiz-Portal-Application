<template>
    <div class="container">
      <div class="user-dashboard">
        <RouterLink to="/userdash" class="icon">
          <i class="fas fa-home"> Home</i>
        </RouterLink>
        <RouterLink to="/uallsubjects" class="icon">
          <i class="fas fa-book circular-icon"> All Subjects</i>
        </RouterLink>
        <RouterLink to="/yourperformance" class="disabled">
          <i class="fas fa-chart-bar"> Your Performance</i>
        </RouterLink>
        <a href="#" @click.prevent="logout" class="icon">
          <i class="fas fa-sign-out-alt"> Log Out</i>
        </a>
      </div>
      <div class="subcontainer">
        <h2>Your Performance</h2>
        <table class="performance-table">
          <thead>
            <tr>
              <th>Subject</th>
              <th>Chapter</th>
              <th>Quiz</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in performance" :key="item.quiz_name + item.subject_name">
              <td>{{ item.subject_name }}</td>
              <td>{{ item.chapter_name }}</td>
              <td>{{ item.quiz_name }}</td>
              <td>{{ item.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "YourPerformance",
    data() {
      return {
        performance: []
      };
    },
    created() {
      this.fetchPerformance();
    },
    methods: {
      async fetchPerformance() {
        try {
          const token = localStorage.getItem("token");
          const response = await axios.get("http://localhost:5000/yourperformance", {
            headers: {
              "Accept": "application/json",
              "Authorization": `Bearer ${token}`
            }
          });
          this.performance = response.data.performance;
        } catch (error) {
          console.error("Error fetching performance:", error);
        }
      },
      logout() {
        localStorage.removeItem("token");
        this.$router.push("/login");
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    font-family: 'Times New Roman', Times, serif;
    display: flex;
    background-color: rgb(213, 213, 213);
    width: 100%;
    height: 100vh;
  }
  .user-dashboard {
    display: flex;
    background-color: rgb(56, 56, 56);
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
    background-color: #000;
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
  .subcontainer {
    margin-left: 10%;
    width: 80%;
    padding: 20px;
    overflow-y: auto;
  }
  .performance-table {
    width: 100%;
    border-collapse: collapse;
  }
  .performance-table th, .performance-table td {
    border: 1px solid #000;
    padding: 10px;
    text-align: left;
  }
  .performance-table th {
    background-color: #f4f4f4;
  }
  </style>
  