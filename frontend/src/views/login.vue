<template>
    <div class="full">
      <div class="image">
        <img src="/bgnormal.jpg" class="img" alt="Background">
      </div>
      <div class="container11">
        <h2>Login</h2>
        <form @submit.prevent="loginUser" class="form">
          <div>
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required />
          </div>
          <div>
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <button type="submit">Login</button>
        </form>
        <div class="links1">
          <RouterLink to="/">Home</RouterLink> |
          <RouterLink to="/signup">SignUp</RouterLink> |
          <RouterLink to="/adminlogin">Not a User? Admin Login</RouterLink>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "UserLogin",
    data() {
      return {
        email: "",
        password: ""
      };
    },
    methods: {
      async loginUser() {
        if (!this.email || !this.password) {
          alert("All fields required");
          return;
        }
        try {
          const response = await fetch("http://localhost:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: this.email, password: this.password })
          });
          const res = await response.json();
          console.log("Raw Response:", response);
          if (res.token) {
            localStorage.setItem("token", res.token);
            alert("Login successful!");
            this.$router.push("/userdash");
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
  
  <style scoped>
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
  .container11 {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: rgb(41, 23, 23) ;
    color: aliceblue;
  }
  .form {
    display: flex;
    flex-direction: column;
    width: 80%;
    max-width: 400px;
    margin-bottom: 20px;
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
  