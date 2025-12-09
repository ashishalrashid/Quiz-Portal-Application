<template>
  <div class="page">
    <aside class="sidebar" aria-label="Admin dashboard navigation">
      <router-link to="/admindash" class="nav-item" title="Home">
        <i class="fas fa-home nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Home</span>
      </router-link>

      <router-link to="/admindash/subjects" class="nav-item" title="Subjects">
        <i class="fas fa-book nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Subjects</span>
      </router-link>

      <router-link to="/admindash/user" class="nav-item" title="Users">
        <i class="fas fa-user nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Users</span>
      </router-link>

      <router-link to="/admindash/stats" class="nav-item" title="Stats">
        <i class="fas fa-chart-bar nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Stats</span>
      </router-link>

      <a href="#" @click.prevent="logout" class="nav-item logout" role="button" title="Log out">
        <i class="fas fa-sign-out-alt nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Log Out</span>
      </a>
    </aside>

    <main class="main">
      <section class="form-card" aria-labelledby="create-question-heading">
        <h2 id="create-question-heading" class="heading">Create Question</h2>

        <form @submit.prevent="createQuestion" class="form" novalidate>
          <div class="field">
            <label for="question" class="label">Question</label>
            <input
              id="question"
              v-model="question"
              type="text"
              class="input"
              required
              placeholder="Type the question text"
              aria-required="true"
            />
          </div>

          <div class="grid">
            <div class="field">
              <label for="option1" class="label">Option 1</label>
              <input id="option1" v-model="option1" type="text" class="input" required placeholder="First option" />
            </div>

            <div class="field">
              <label for="option2" class="label">Option 2</label>
              <input id="option2" v-model="option2" type="text" class="input" required placeholder="Second option" />
            </div>

            <div class="field">
              <label for="option3" class="label">Option 3</label>
              <input id="option3" v-model="option3" type="text" class="input" required placeholder="Third option" />
            </div>

            <div class="field">
              <label for="option4" class="label">Option 4</label>
              <input id="option4" v-model="option4" type="text" class="input" required placeholder="Fourth option" />
            </div>
          </div>

          <div class="field small">
            <label for="answer" class="label">Answer (option number)</label>
            <input
              id="answer"
              v-model.number="answer"
              type="number"
              class="input"
              required
              min="1"
              max="4"
              placeholder="1 - 4"
              aria-required="true"
            />
            <small class="hint">Enter the option number (1–4) that is the correct answer.</small>
          </div>

          <div class="actions">
            <button type="submit" class="btn-primary">Create</button>
            <router-link :to="`/quiz/${$route.params.quiz_id || ''}`" class="btn-secondary">Cancel</router-link>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CreateQuestion",
  data() {
    return {
      question: "",
      option1: "",
      option2: "",
      option3: "",
      option4: "",
      answer: null
    };
  },
  methods: {
    async createQuestion() {
      if (!this.question || !this.option1 || !this.option2 || !this.option3 || !this.option4 || this.answer == null) {
        alert("All fields are required!");
        return;
      }
      try {
        const token = localStorage.getItem("token");
        const quizId = this.$route.params.quiz_id;
        const response = await axios.post(
          `http://localhost:5000/createquestion/${quizId}`,
          {
            question: this.question,
            option1: this.option1,
            option2: this.option2,
            option3: this.option3,
            option4: this.option4,
            answer: this.answer
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
            }
          }
        );
        console.log("Question created successfully:", response.data);
        this.$router.push(`/quiz/${quizId}`);
      } catch (error) {
        console.error("Error:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
:root {
  --sidebar-bg: #1f2933;
  --accent: #0f4c5c;
  --muted: #6b7280;
  --card-bg: #ffffff;
  --radius: 12px;
  --gap: 14px;
  --max-width: 920px;
  --container-padding: 20px;
}

.page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(180deg, #f3f5f6 0%, #e9ecef 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: #0b1220;
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: var(--sidebar-bg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 2px 0 8px rgba(2,6,23,0.08);
  align-items: stretch;
}
.nav-item {
  display: flex;
  gap: 12px;
  align-items: center;
  text-decoration: none;
  color: #e6eef1;
  padding: 10px 12px;
  border-radius: 10px;
  transition: transform 120ms ease, background-color 120ms ease;
  font-weight: 600;
  font-size: 0.98rem;
}
.nav-item .nav-icon {
  width: 28px;
  text-align: center;
  font-size: 1.05rem;
  opacity: 0.95;
}
.nav-item .nav-label {
  display: inline-block;
}
.nav-item:hover,
.nav-item:focus {
  background: rgba(255,255,255,0.04);
  transform: translateY(-2px);
  outline: none;
}
.logout {
  margin-top: auto;
  background: rgba(255,255,255,0.02);
}
.logout:hover {
  background: rgba(255,255,255,0.06);
}

/* Main */
.main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: var(--container-padding);
  gap: var(--gap);
}

/* Card */
.form-card {
  width: 100%;
  max-width: var(--max-width);
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: 0 6px 18px rgba(16,24,40,0.06);
  margin-top: 72px;
}

/* Heading */
.heading {
  margin: 0 0 14px 0;
  font-size: 1.5rem;
  color: #0b1220;
}

/* Form layout */
.form {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field.small { max-width: 220px; }

/* Labels and inputs */
.label {
  font-size: 0.9rem;
  color: var(--muted);
  font-weight: 600;
}

.input {
  height: 44px;
  padding: 0 12px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  background: #fbfdff;
  font-size: 1rem;
  color: #0b1220;
  transition: box-shadow 120ms ease, border-color 120ms ease, transform 120ms ease;
  outline: none;
}
.input::placeholder { color: #9ca3af; }
.input:focus {
  border-color: var(--accent);
  box-shadow: 0 4px 14px rgba(15,76,92,0.08);
  transform: translateY(-1px);
}

/* hint text */
.hint {
  font-size: 0.82rem;
  color: #8b8f98;
}

/* Actions */
.actions {
  display: flex;
  gap: 12px;
  margin-top: 6px;
  align-items: center;
}

.btn-primary {
  background: linear-gradient(180deg, var(--accent), #083b45);
  color: #fff;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease, opacity 120ms ease;
}
.btn-primary:hover,
.btn-primary:focus {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(15,76,92,0.18);
}
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #0b1220;
  background: #f3f4f6;
  border: 1px solid #e6e9eb;
  font-weight: 600;
}
.btn-secondary:hover { background: #eef2f6; transform: translateY(-2px); }

/* Responsive */
@media (max-width: 880px) {
  .sidebar { width: 64px; padding: 14px 8px; gap: 6px; }
  .nav-item .nav-label { display: none; }
  .grid { grid-template-columns: 1fr; }
  .form-card { margin-top: 20px; padding: 18px; }
}
</style>
