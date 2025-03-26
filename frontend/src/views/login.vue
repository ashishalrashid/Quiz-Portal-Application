<template>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
        <div>
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required />
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
    </div>
</template>


<script>
export default{
    data(){
        return{
            email:"",
            password:"",
        };
    },
    methods:{
        async loginUser(){
            if (!this.email || !this.password){
                alert("All fields requeired");
                return;
            }

            try{
                const response =await fetch("https://localhost:5000/login",{
                    methods:"POST",
                    headers:{"Content-Type":"application/json"},
                    body:JSON.stringify({email:this.email,password:this.password})
                });

                const res =await response.json();
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