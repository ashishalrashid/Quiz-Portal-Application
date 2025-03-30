<template>
    <div class="container">
      <div class="user-dashboard">
        <RouterLink to="/userdash" class="icon">
          <i class="fas fa-home"> Home</i>
        </RouterLink>
        <RouterLink to="/uallsubjects" class="icon">
          <i class="fas fa-book circular-icon"> All Subjects</i>
        </RouterLink>
        <RouterLink to="/yourperformance" class="icon">
          <i class="fas fa-chart-bar"> Your Performance</i>
        </RouterLink>
        <a href="#" @click.prevent="logout" class="icon">
          <i class="fas fa-sign-out-alt"> Log Out</i>
        </a>
      </div>
      <div class="subcontainer">
        <h2>Active Quizzes</h2>
        <table class="quiz-table">
          <thead>
            <tr>
              <th>Quiz Name</th>
              <th>Chapter Name</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in quizzes" :key="quiz.id">
              <td>{{ quiz.quiz_name }}</td>
              <td>{{ quiz.chapter_name }}</td>
              <td>{{ quiz.start_date }}</td>
              <td>{{ quiz.end_date }}</td>
              <td>
                <button @click="goToQuiz(quiz.id)" class="but">Go To Quiz</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ActiveQuizzes",
    data() {
      return {
        quizzes: []
      };
    },
    created() {
      this.fetchQuizzes();
    },
    methods: {
      async fetchQuizzes() {
        try {
          const token = localStorage.getItem("token");
          const subjectId = this.$route.params.subject_id;
          const response = await fetch(`http://localhost:5000/getuserquizzes/${subjectId}`, {
            headers: {
              "Accept": "application/json",
              "Authorization": "Bearer " + token
            }
          });
          if (!response.ok) {
            throw new Error("Failed to fetch active quizzes");
          }
          const data = await response.json();
          this.quizzes = data.quizzes;
        } catch (error) {
          console.error("Error fetching active quizzes:", error);
        }
      },
      goToQuiz(quizId) {
        this.$router.push(`/takequiz/${quizId}`);
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
    overflow-y: auto;
  }
  .quiz-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  .quiz-table th, .quiz-table td {
    border: 1px solid #000;
    padding: 10px;
    text-align: left;
    height: 50px;
    vertical-align: middle;
  }
  .quiz-table th {
    background-color: #f4f4f4;
  }
  .but {
    background-color: #fff;
    border: 1px solid #000;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
  }
  </style>
  