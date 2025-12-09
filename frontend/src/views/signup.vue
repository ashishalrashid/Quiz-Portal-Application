<template>
  <div class="page">
    <main class="card" role="main" aria-labelledby="signup-heading">
      <h2 id="signup-heading" class="title">Create an account</h2>

      <form @submit.prevent="signupUser" class="form" novalidate>
        <label for="username" class="label">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          class="input"
          required
          placeholder="Choose a username"
          aria-required="true"
        />

        <label for="email" class="label">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="input"
          required
          placeholder="you@example.com"
          aria-required="true"
        />

        <label for="password" class="label">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="input"
          required
          placeholder="At least 8 characters"
          aria-required="true"
        />

        <div class="actions">
          <button type="submit" class="btn-primary">Sign Up</button>
          <router-link to="/login" class="btn-secondary">Already have an account?</router-link>
        </div>
      </form>

      <nav class="footer-links" aria-label="primary navigation">
        <router-link to="/" class="link">Home</router-link>
      </nav>
    </main>
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

<style scoped>
:root {
  --card-bg: #ffffff;
  --accent: #0f4c5c;
  --muted: #6b7280;
  --radius: 12px;
  --max-width: 520px;
}

* { box-sizing: border-box; }

.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg,#f3f5f6,#e9ecef);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
  padding: 24px;
  color: #0b1220;
}

.card {
  width: 100%;
  max-width: var(--max-width);
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: 0 12px 30px rgba(11,23,40,0.06);
}

.title {
  margin: 0 0 14px 0;
  font-size: 1.4rem;
  font-weight: 700;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 6px;
}

.label {
  font-size: 0.9rem;
  color: var(--muted);
  font-weight: 600;
}

.input {
  height: 44px;
  padding: 0 12px;
  border-radius: 10px;
  border: 1px solid #e6e9eb;
  background: #fbfdff;
  font-size: 1rem;
  outline: none;
  transition: box-shadow 120ms ease, border-color 120ms ease, transform 120ms ease;
}

.input::placeholder { color: #9ca3af; }

.input:focus {
  border-color: var(--accent);
  box-shadow: 0 8px 20px rgba(15,76,92,0.06);
  transform: translateY(-1px);
}

.actions {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 8px;
}

.btn-primary {
  background: linear-gradient(180deg,var(--accent), #083b45);
  color: #fff;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #0b1220;
  background: #f3f4f6;
  border: 1px solid #e6e9eb;
  font-weight: 600;
}

.footer-links {
  margin-top: 18px;
  display: flex;
  gap: 12px;
  justify-content: flex-start;
}

.link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
}

@media (max-width: 560px) {
  .card { padding: 18px; }
  .actions { flex-direction: column; align-items: stretch; }
  .btn-secondary { justify-content: center; }
}
</style>
