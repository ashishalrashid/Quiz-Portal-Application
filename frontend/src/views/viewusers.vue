<template>
    <div class="container">
      <div class="admin-dashboard">
        <RouterLink to="/admindash" class="icon">
          <i class="fas fa-home"> Home</i>
        </RouterLink>
        <RouterLink to="/admindash/subjects" class="icon">
          <i class="fas fa-book circular-icon"> Subjects</i>
        </RouterLink>
        <RouterLink to="/admindash/user" class="disabled">
          <i class="fas fa-user circular-icon"> Users</i>
        </RouterLink>
        <RouterLink to="/admindash/stats" class="icon">
          <i class="fas fa-chart-bar"> Stats</i>
        </RouterLink>
        <a href="#" @click.prevent="logout" class="icon">
          <i class="fas fa-sign-out-alt"> Log Out</i>
        </a>
      </div>
      <div class="acont">
      <div class="top">
    <h2>Users</h2>
    <input type="text" v-model="searchQuery" placeholder="Search users..." class="field"/>
    <button @click="searchUsers" class="search-btn">
        <i class="fas fa-search"></i> Search
    </button>
</div>

        
        <table class="user-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Full Name</th>
              <th>Qualification</th>
              <th>Date of Birth</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.full_name }}</td>
              <td>{{ user.qualification }}</td>
              <td>{{ user.dob }}</td>
              <td class="action-buttons">
                <button @click="deleteUser(user.id)" class="danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "Users",
    data() {
      return {
        users: []
      };
    },
    created() {
      this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const token = localStorage.getItem("token");
          const response = await axios.get("http://localhost:5000/getusers", {
            headers: {
              "Accept": "application/json",
              Authorization: `Bearer ${token}`
            }
          });
          this.users = response.data;
        } catch (error) {
          console.error("Error fetching users:", error);
        }
      },
      async deleteUser(userId) {
        try {
          const token = localStorage.getItem("token");
          await axios.delete(`http://localhost:5000/deleteuser/${userId}`, {
            headers: {
              "Accept": "application/json",
              Authorization: `Bearer ${token}`
            }
          });
          this.fetchUsers();
        } catch (error) {
          console.error("Error deleting user:", error);
        }
      },
      async searchUsers() {
  try {
    const response = await fetch("http://localhost:5000/getsearchuser", {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("token")
      },
      body: JSON.stringify({ pattern: this.searchQuery })
    });

    if (!response.ok) {
      throw new Error("Failed to search users");
    }

    const data = await response.json();
    this.users = data.users;
  } catch (error) {
    console.error("Error searching users:", error);
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
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 10px;
    border-radius: 250px;
    margin: 10px;
    color: white;
    width: 80%;
    font-family: 'Times New Roman', Times, serif;
    text-decoration: None !important;
  }
  .icon:hover {
    background-color: #000000;
    transform: scale(1.1);
  }
  .subcontainer {
    margin-left: 10%;
    width: 80%;
    overflow-y: auto;
  }
  .user-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  .user-table th, .user-table td {
    border: 1px solid black;
    padding: 10px;
    text-align: left;
    height: 50px;
    vertical-align: middle;
  }
  .user-table th {
    background-color: #f4f4f4;
  }
  .action-buttons {
    display: flex;
    gap: 10px;
  }
  .danger {
    background-color: red;
    border: none;
    color: white;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
  }
  .acont{
    display: flex;
    flex-direction: column;
    margin: auto;
  }
  </style>
  