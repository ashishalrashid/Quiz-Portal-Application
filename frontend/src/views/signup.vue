<template>
    <h2>Signup</h2>
    <form @submit.prevent="signupUser">
      <div>
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Sign Up</button>
    </form>
  
    <div>
      <RouterLink to="/">Home</RouterLink> | 
      <RouterLink to="/login">Login</RouterLink>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        username: "",
        email: "",
        password: "",
      };
    },
    methods: {
      async signupUser() {
        if (!this.username || !this.email || !this.password) {
          alert("All fields are required!");
          return;
        }
        try {
          const response = await axios.post("http://localhost:5000/signup", {
            username: this.username,
            email: this.email,
            password: this.password,
          });
          alert(response.data.message || "Signup Successful");
          this.$router.push("/login");
        } catch (error) {
          alert(error.response?.data?.message || "Signup failed");
        }
      },
    },
  };
  </script>
  