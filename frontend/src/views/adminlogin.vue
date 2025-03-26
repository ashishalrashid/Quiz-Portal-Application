<template>
    <h2>Login</h2>
    <form @submit.prevent="loginAdmin">
        <div>
            <label for="username">Admin Username</label>
            <input type="text" id="username" v-model="username" required />
        </div>
        <div>
            <label for="password">Password</label>
            <input type="password"  id="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
    </form>

    <div>
        <RouterLink to="/">Home</RouterLink> |
        <RouterLink to="/signup">SignUp</RouterLink>
        <RouterLink to="/login">Not an Admin ? User Login</RouterLink>

    </div>
</template>


<script>
export default{
    data(){
        return{
            username:"",
            password:"",
        };
    },
    methods:{
        async loginUser(){
            if (!this.username || !this.password){
                alert("All fields requeired");
                return;
            }

            try{
                const response =await fetch("http://localhost:5000/adminlogin",{
                    method:"POST",
                    headers:{"Content-Type":"application/json"},
                    body:JSON.stringify({username:this.username,password:this.password})
                });

                const res =await response.json();
                console.log("Raw Response:", response);
                if (res.token){
                    localStorage.setItem("token",res.token);
                    alert("login sucessful!");
                    this.$router.push("/userdash");
                }else{
                    alert("Invalid Login");
                }
                } catch(error){
                    alert("Login Failed");
                }
                }
            }
        }
</script>