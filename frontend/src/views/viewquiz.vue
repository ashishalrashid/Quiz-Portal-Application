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
        <RouterLink to="/admindash/stats" class="icon">
          <i class="fas fa-chart-bar"> Stats</i>
        </RouterLink>
        <a href="#" @click.prevent="logout" class="icon">
          <i class="fas fa-sign-out-alt"> Log Out</i>
        </a>
      </div>
      <div class="subcontainer">
        <div class="top">
        <h2>Questions</h2>
        <input type="text" v-model="searchQuery" placeholder="Search..." class="field" />
        <button @click="searchQuestions" class="search-btn">
          <i class="fas fa-search"></i>
        </button>
      </div>
        <table class="question-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Question</th>
              <th>Options</th>
              <th>Answer</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="question in questions" :key="question.id">
              <td>{{ question.id }}</td>
              <td>{{ question.question }}</td>
              <td>
                <ul>
                  <li v-for="(option, index) in question.options" :key="index">{{ option }}</li>
                </ul>
              </td>
              <td>{{ question.answer }}</td>
              <td class="action-buttons">
                <button @click="goToEditQuestion(question.id)" class="but">Edit</button>
                <button @click="deleteQuestion(question.id)" class="danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
        <button @click="goToCreateQuestion" class="create-button">
          <i class="fas fa-plus-circle"></i> Create Question
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "Questions",
    data() {
      return {
        questions: []
      };
    },
    created() {
      this.fetchQuestions();
    },
    methods: {
      async fetchQuestions() {
        try {
          const quizId = this.$route.params.quiz_id;
          const response = await fetch(`http://localhost:5000/getquestion/${quizId}`, {
            headers: {
              "Accept": "application/json",
              "Authorization": "Bearer " + localStorage.getItem("token")
            }
          });
          if (!response.ok) {
            throw new Error("Failed to fetch questions");
          }
          const data = await response.json();
          this.questions = data;
        } catch (error) {
          console.error("Error fetching questions:", error);
        }
      },
      logout() {
        localStorage.removeItem("token");
        this.$router.push("/login");
      },
      goToEditQuestion(questionId) {
        this.$router.push(`/question/${questionId}/edit`);
      },
      deleteQuestion(questionId) {
        axios.delete(`http://localhost:5000/deletequestion/${questionId}`, {
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        })
        .then(() => {
          this.fetchQuestions();
        })
        .catch(error => {
          console.error("Error deleting question:", error);
        });
      },
      async searchQuestions() {
  const quizId = this.$route.params.quiz_id;
  try {
    const response = await fetch(`http://localhost:5000/getsearchquestions/${quizId}`, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("token")
      },
      body: JSON.stringify({ pattern: this.searchQuery })
    });

    if (!response.ok) {
      throw new Error("Failed to search questions");
    }

    const data = await response.json();
    this.questions = data.questions;
  } catch (error) {
    console.error("Error searching questions:", error);
  }
},


      goToCreateQuestion() {
        const quizId = this.$route.params.quiz_id;
        this.$router.push(`/createquestion/${quizId}`);
      }
    }
  };
  </script>
  
  <style>
  html, body, #app {
    margin: 0;
  }
  .container {
    font-family: 'Times New Roman', Times, serif;
    display: flex;
    background-color: rgb(213, 213, 213);
    height: 100vh;
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
    display: flexbox;
    justify-content: center;
    align-items: flex-start;
    padding: 10px;
    border-radius: 250px;
    margin: 10px;
    color: rgb(255, 255, 255);
    width: 80%;
    font-family: 'Times New Roman', Times, serif;
  }
  .icon:hover {
    background-color: #000000;
    transform: scale(1.1);
  }
  .subcontainer {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 10%;
    overflow-y: auto;
    width: 80%;
  }
  .question-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  .question-table th, .question-table td {
    border: 1px solid black;
    padding: 10px;
    text-align: left;
  }
  .question-table th {
    background-color: #f4f4f4;
  }
  .question-table th,
.question-table td {
  height: 50px;
  vertical-align: middle;
}
  .action-buttons {
    display: flex;
    gap: 10px;
  }
  .but {
    background-color: #ffffff;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
  }
  .danger {
    background-color: red;
    border: none;
    color: white;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
  }
  .create-button {
    background-color: #003f54;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 25px;
    margin-top: 20px;
    cursor: pointer;
    font-size: 1em;
  }
  .create-button i {
    margin-right: 8px;
  }
  </style>
  