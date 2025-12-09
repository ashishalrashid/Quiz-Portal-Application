<template>
  <div class="page">
    <div class="split">
      <div class="visual">
        <img src="/bgnormal.jpg" alt="Background" class="visual-img" />
        <div class="visual-overlay" aria-hidden="true"></div>
      </div>

      <main class="panel" role="main" aria-labelledby="user-login-heading">
        <h2 id="user-login-heading" class="panel-title">Login</h2>

        <form @submit.prevent="loginUser" class="login-form" novalidate>
          <label for="email" class="label">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="input"
            placeholder="you@example.com"
            aria-required="true"
          />

          <label for="password" class="label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="input"
            placeholder="Enter your password"
            aria-required="true"
          />

          <button type="submit" class="btn">Login</button>
        </form>

        <div class="links">
          <router-link to="/" class="link">Home</router-link>
          <span class="sep">|</span>
          <router-link to="/signup" class="link">Sign Up</router-link>
          <span class="sep">|</span>
          <router-link to="/adminlogin" class="link">Not a User? Admin Login</router-link>
        </div>
      </main>
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
:root{
  --bg-start:#0f1724;
  --bg-end:#082032;
  --panel-bg:#ffffff;
  --accent:#0f4c5c;
  --muted:#6b7280;
  --radius:12px;
  --gap:16px;
}

*{box-sizing:border-box}

.page{
  min-height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  background: linear-gradient(180deg,var(--bg-start),var(--bg-end));
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
  padding:20px;
  color:#0b1220;
}

.split{
  width:100%;
  max-width:1100px;
  height:72vh;
  display:grid;
  grid-template-columns: 1fr 460px;
  gap:24px;
  align-items:stretch;
}

.visual{
  position:relative;
  border-radius:var(--radius);
  overflow:hidden;
  box-shadow: 0 10px 30px rgba(2,6,23,0.45);
}

.visual-img{
  width:100%;
  height:100%;
  object-fit:cover;
  display:block;
  transform:scale(1.02);
}

.visual-overlay{
  position:absolute;
  inset:0;
  background: linear-gradient(180deg, rgba(6,21,34,0.28), rgba(6,21,34,0.6));
}

.panel{
  background:var(--panel-bg);
  border-radius:var(--radius);
  padding:28px;
  box-shadow: 0 10px 30px rgba(2,6,23,0.08);
  display:flex;
  flex-direction:column;
  justify-content:center;
}

.panel-title{
  margin:0 0 18px;
  font-size:1.5rem;
  color:#0b1220;
  text-align:left;
}

.login-form{
  display:flex;
  flex-direction:column;
  gap:12px;
  width:100%;
  max-width:360px;
}

.label{
  font-size:0.9rem;
  color:var(--muted);
  font-weight:600;
}

.input{
  height:44px;
  padding:8px 12px;
  border-radius:10px;
  border:1px solid #e6e9eb;
  font-size:1rem;
  background:#fbfdff;
  transition: box-shadow 120ms ease, border-color 120ms ease, transform 120ms ease;
  outline:none;
}

.input:focus{
  border-color:var(--accent);
  box-shadow: 0 8px 20px rgba(15,76,92,0.08);
  transform: translateY(-2px);
}

.btn{
  margin-top:6px;
  padding:10px 14px;
  border-radius:10px;
  background: linear-gradient(180deg,var(--accent), #083b45);
  color:#fff;
  border:none;
  font-weight:700;
  cursor:pointer;
  transition: transform 120ms ease, box-shadow 120ms ease;
}

.btn:hover,
.btn:focus{
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(11,23,40,0.12);
}

.links{
  margin-top:18px;
  display:flex;
  justify-content:center;
  gap:8px;
  flex-wrap:wrap;
}

.link{
  color:var(--accent);
  text-decoration:none;
  font-weight:600;
}

.sep{
  color:#c7ccd1;
}

@media (max-width:980px){
  .split{ grid-template-columns: 1fr; height:auto; }
  .visual{ order:1; height:220px; }
  .panel{ order:2; margin-top:16px; }
  .page{ padding:16px; }
}
</style>
