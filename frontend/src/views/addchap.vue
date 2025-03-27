<template>
    <div class="container">
    <div class="admin-dashboard">
              <RouterLink to="/admindash" class="icon">
                <i class="fas fa-home"> Home</i>
              </RouterLink>
              <RouterLink to="/admindash/subjects" class="icon">
                <i class="fas fa-book circular-icon">  Subjects</i>
              </RouterLink>
              <RouterLink to="/admindash/user" class="icon">
                <i class="fas fa-user circular-icon">  Users</i>
                </RouterLink>
              <RouterLink to="/admindash/stats" class="icon">
                <i class="fas fa-chart-bar">  Stats</i>
              </RouterLink>
              <a href="#" @click.prevent="logout" class="icon">
                <i class="fas fa-sign-out-alt">  Log Out</i>
              </a>
    </div>
    <div class="form-container">
    <h2>Create Chapter</h2>
    <form @submit.prevent="NewSub" class="from">
      <div>
        <label for="Sub_name">Chapter Name:   </label>
        <input type="text" id="Sub_name" v-model="Sub_name" required />
      </div>
      <div>
        <label for="description">Description:   </label>
        <input type="text" id="description" v-model="description" required />
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
        Sub_name: "",
        description: "",
      };
    },
    methods: {
        async NewSub() {
  if (!this.Sub_name || !this.description) {
    alert("All fields are required!");
    return;
  }
  
  try {
    const token = localStorage.getItem("token");
    const subjectId = this.$route.params.subject_id
    const response = await axios.post(
      `http://localhost:5000/createchapter/${subjectId}`,
      {
        name: this.Sub_name,
        description: this.description,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, 
        },
      }
    );

    console.log("Subject created successfully:", response.data);
    this.$router.push(`/admindash/subject/${subjectId}`);
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
      margin:10px;
      color: rgb(255, 255, 255);
      width: 80%;
      font-family: 'Times New Roman', Times, serif;
  }
  .icon:hover {
    background-color: #000000;
    transform: scale(1.1);
  }
  .disabled{
      background-color: rgb(117, 116, 116);
      padding: 10px;
      border-radius: 250px;
      margin:10px;
      width: 80%;
      color:aliceblue;
  }
  .subcontainer {
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      margin-left: 10%;
      width: 100%;
  }
  .subs {
      display: flex;
      justify-content: space-around;
      list-style: none;
      height: 300px !important;
  
  }
  .sub_item {
    border: 1px solid #040404;
    border-radius: 25px;
    padding: 15px;
    cursor: pointer;
    margin: 10px;
    width: 40%;
  }
  .sub_item:hover {
    background-color: #ffffff;
    transform: scale(1.05);
  }
  
  .all-subjects {
    text-decoration: none;
    color: #fff; 
    background-color: #003f54; 
    padding: 10px 15px;
    border: none;
    border-radius: 25px;
    display: inline-flex;
    align-items: center;
    cursor: pointer;
    font-size: 1em;
    margin-bottom: auto;
  }
  
  .all-subjects i {
    margin-left: 8px;
  }
  .count{
      display: flex;;
      justify-content: space-around;
      height: 100%;
  }
  .subject-list {
    margin: 0px;
  }
  
  .sta {
      list-style: none;
      border: 1px solid #040404;
      border-radius: 25px;
      padding: 10px;
      margin: 10px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 30%;
      height: 100%;
  }
  .sta:hover {
      transform: scale(1.05);
  }
  
  .stat .big-number {
    font-size: 3em;
    font-weight: bold;
    color: #003f54;
    text-decoration: none;
  
  }
.form-container {
    margin: auto;
    margin-top: 100px;
    border: 1px ;
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
  .from input{
    border-radius: 25px;
  }
  .from button {
    background-color: #003f54;
    border-radius: 25px;
    color: #fff;
    padding: 5px;
    border: 1px solid black;
  }
  .from:hover button {
    background-color: #000000;
    transform: scale(1.1);
}

  </style>