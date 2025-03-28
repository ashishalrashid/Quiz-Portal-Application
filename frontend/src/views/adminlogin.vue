<template>
    <div class="full">
      <div class="image">
        <img src="/bgimage.jpg" class="img" alt="Background">
      </div>
      <div class="container1">
        <h2>Admin Login</h2>
        <form @submit.prevent="loginAdmin" class="form">
          <div>
            <label for="username">Admin Username:</label>
            <input type="text" id="username" v-model="username" required />
          </div>
          <div>
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <button type="submit">Login</button>
        </form>
        <div class="links1">
          <RouterLink to="/">Home</RouterLink> |
          <RouterLink to="/signup">SignUp</RouterLink> |
          <RouterLink to="/login">Not an Admin? User Login</RouterLink>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: "",
        password: "",
      };
    },
    methods: {
      async loginAdmin() {
        if (!this.username || !this.password) {
          alert("All fields required");
          return;
        }
        try {
          const response = await fetch("http://localhost:5000/adminlogin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: this.username, password: this.password })
          });
          const res = await response.json();
          console.log("Raw Response:", response);
          if (res.token) {
            localStorage.setItem("token", res.token);
            alert("Login successful!");
            this.$router.push("/admindash");
          } else {
            alert("Invalid Login");
          }
        } catch (error) {
          alert("Login Failed");
        }
      }
    }
  };
  </script>
  
  <style>
  html, body, #app {
    margin: 0;
    width: 100%;
    height: 100%;
  }
  .full {
    display: flex;
    width: 100%;
    height: 100vh;
  }
  .image {
    flex: 1;
    overflow: hidden;
  }
  .img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .container1 {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #3a0000 !important; 
    color: aliceblue;
    border-radius: 0px;
  }
  .form {
    display: flex;
    flex-direction: column;
    width: 80%;
    max-width: 400px;
  }
  .form div {
    margin: 10px 0;
  }
  .form input {
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #000;
  }
  .form button {
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #003f54;
    color: #fff;
    cursor: pointer;
    margin-top: 10px;
  }
  .form button:hover {
    background-color: #000;
  }
  .links1 {
    margin-top: 20px;
    text-align: center;
  }
  .links1 a {
    color: #fff;
    text-decoration: none;
    margin: 0 5px;
  }
  .links1 a:hover {
    color: rgb(186, 171, 253);
  }
  </style>
  