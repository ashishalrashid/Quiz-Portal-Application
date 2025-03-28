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
      <div class="form-container">
        <h2>Create Question</h2>
        <form @submit.prevent="createQuestion" class="from">
          <div>
            <label for="question">Question: </label>
            <input type="text" id="question" v-model="question" required />
          </div>
          <div>
            <label for="option1">Option 1: </label>
            <input type="text" id="option1" v-model="option1" required />
          </div>
          <div>
            <label for="option2">Option 2: </label>
            <input type="text" id="option2" v-model="option2" required />
          </div>
          <div>
            <label for="option3">Option 3: </label>
            <input type="text" id="option3" v-model="option3" required />
          </div>
          <div>
            <label for="option4">Option 4: </label>
            <input type="text" id="option4" v-model="option4" required />
          </div>
          <div>
            <label for="answer">Answer (option number): </label>
            <input type="number" id="answer" v-model.number="answer" required min="1" max="4" />
          </div>
          <button type="submit" class="mit">Create</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "CreateQuestion",
    data() {
      return {
        question: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        answer: null
      };
    },
    methods: {
      async createQuestion() {
        if (!this.question || !this.option1 || !this.option2 || !this.option3 || !this.option4 || this.answer == null) {
          alert("All fields are required!");
          return;
        }
        try {
          const token = localStorage.getItem("token");
          const quizId = this.$route.params.quiz_id;
          const response = await axios.post(
            `http://localhost:5000/createquestion/${quizId}`,
            {
              question: this.question,
              option1: this.option1,
              option2: this.option2,
              option3: this.option3,
              option4: this.option4,
              answer: this.answer
            },
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
              }
            }
          );
          console.log("Question created successfully:", response.data);
          this.$router.push(`/quiz/${quizId}`);
        } catch (error) {
          console.error("Error:", error);
        }
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
    display: flexbox;
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
  .form-container {
    margin: auto;
    margin-top: 100px;
    border-radius: 25px;
    background-color: #ffffff;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 60%;
    overflow-y: auto;
  }
  .from {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
  }
  .from div {
    margin: 10px;
  }
  .from input {
    border-radius: 25px;
    padding: 5px;
    border: 1px solid black;
  }
  .from button {
    background-color: #003f54;
    border-radius: 25px;
    color: white;
    padding: 5px;
    border: 1px solid black;
  }
  .from:hover button {
    background-color: #000000;
    transform: scale(1.1);
  }
  </style>
  