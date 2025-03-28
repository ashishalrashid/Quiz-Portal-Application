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
        <h2>Edit Chapter</h2>
        <form @submit.prevent="updateChapter" class="from">
          <div>
            <label for="chapterName">Chapter Name: </label>
            <input type="text" id="chapterName" v-model="chapterName" />
          </div>
          <div>
            <label for="description">Description: </label>
            <input type="text" id="description" v-model="description" />
          </div>
          <button type="submit" class="mit">Update</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "EditChapter",
    data() {
      return {
        chapterName: "",
        description: ""
      };
    },
    created() {
      this.fetchChapter();
    },
    methods: {
      async fetchChapter() {
        try {
          const chapterId = this.$route.params.chapter_id;
          const token = localStorage.getItem("token");
          const response = await axios.get(`http://localhost:5000/getchapter/${chapterId}`, {
            headers: {
              "Accept": "application/json",
              Authorization: `Bearer ${token}`
            }
          });
          this.chapterName = response.data.chapter.name;
          this.description = response.data.chapter.description;
        } catch (error) {
          console.error("Error fetching chapter:", error);
        }
      },
      async updateChapter() {
        try {
          const chapterId = this.$route.params.chapter_id;
          const token = localStorage.getItem("token");
          const data = {
            name: this.chapterName,
            description: this.description
          };
          const response = await axios.put(`http://localhost:5000/editchapter/${chapterId}`, data, {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
            }
          });
          console.log("Chapter updated successfully:", response.data);
          this.$router.push(`/admindash/subject/${chapterId}`);
        } catch (error) {
          console.error("Error updating chapter:", error);
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
  