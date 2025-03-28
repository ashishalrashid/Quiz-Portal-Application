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
        <h2>Create Quiz</h2>
        <form @submit.prevent="createQuiz" class="from">
          <div>
            <label for="name">Quiz Name: </label>
            <input type="text" id="name" v-model="name" required />
          </div>
          <div>
            <label for="start_date">Start Date: </label>
            <input type="date" id="start_date" v-model="start_date" required />
          </div>
          <div>
            <label for="end_date">End Date: </label>
            <input type="date" id="end_date" v-model="end_date" required />
          </div>
          <div>
            <label for="time_duration">Duration (minutes): </label>
            <input type="number" id="time_duration" v-model="time_duration" required />
          </div>
          <button type="submit" class="mit">Create</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        name: "", // Added name field
        start_date: "",
        end_date: "",
        time_duration: 20,
      };
    },
    methods: {
      async createQuiz() {
        if (!this.name || !this.start_date || !this.end_date || !this.time_duration) {
          alert("All fields are required!");
          return;
        }
        try {
          const token = localStorage.getItem("token");
          const chapterId = this.$route.params.chapter_id;
          const response = await axios.post(
            `http://localhost:5000/createquiz/${chapterId}`,
            {
              name: this.name, // Send quiz name to backend
              start_date: this.start_date,
              end_date: this.end_date,
              time_duration: this.time_duration,
            },
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          );
          console.log("Quiz created successfully:", response.data);
          this.$router.push(`/admindash/chapter/${chapterId}`);
        } catch (error) {
          console.error("Error:", error);
        }
      },
    },
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
  