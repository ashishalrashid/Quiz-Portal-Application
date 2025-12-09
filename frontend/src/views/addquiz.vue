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
      <section class="form-card" aria-labelledby="create-quiz-heading">
        <h2 id="create-quiz-heading" class="heading">Create Quiz</h2>

        <form @submit.prevent="createQuiz" class="form" novalidate>
          <div class="field">
            <label for="name" class="label">Quiz Name</label>
            <input
              id="name"
              v-model="name"
              type="text"
              class="input"
              required
              placeholder="e.g. Midterm - Chapter 3"
              aria-required="true"
            />
          </div>

          <div class="row">
            <div class="field">
              <label for="start_date" class="label">Start Date</label>
              <input id="start_date" v-model="start_date" type="date" class="input" required aria-required="true" />
            </div>

            <div class="field">
              <label for="end_date" class="label">End Date</label>
              <input id="end_date" v-model="end_date" type="date" class="input" required aria-required="true" />
            </div>
          </div>

          <div class="field small">
            <label for="time_duration" class="label">Duration (minutes)</label>
            <input
              id="time_duration"
              v-model.number="time_duration"
              type="number"
              class="input"
              required
              min="1"
              placeholder="20"
              aria-required="true"
            />
            <small class="hint">Enter total minutes for the quiz</small>
          </div>

          <div class="actions">
            <button type="submit" class="btn-primary">Create</button>
            <router-link :to="`/chapter/${$route.params.chapter_id || ''}`" class="btn-secondary">Cancel</router-link>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "", // Added name field
      start_date: "",
      end_date: "",
      time_duration: 20,
    };
  },
  methods: {
    async createQuiz() {
      if (!this.name || !this.start_date || !this.end_date || !this.time_duration) {
        alert("All fields are required!");
        return;
      }
      try {
        const token = localStorage.getItem("token");
        const chapterId = this.$route.params.chapter_id;
        const response = await axios.post(
          `http://localhost:5000/createquiz/${chapterId}`,
          {
            name: this.name,
            start_date: this.start_date,
            end_date: this.end_date,
            time_duration: this.time_duration,
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log("Quiz created successfully:", response.data);
        this.$router.push(`/chapter/${chapterId}`);
      } catch (error) {
        console.error("Error:", error);
      }
    },
  },
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

.row {
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
  .row { grid-template-columns: 1fr; }
  .form-card { margin-top: 20px; padding: 18px; }
}
</style>
