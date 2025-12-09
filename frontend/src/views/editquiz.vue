<template>
  <div class="page">
    <aside class="sidebar" aria-label="Admin navigation">
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

    <main class="main" role="main">
      <section class="card" aria-labelledby="edit-quiz-heading">
        <h2 id="edit-quiz-heading" class="heading">Edit Quiz</h2>

        <form @submit.prevent="updateQuiz" class="form" novalidate>
          <label for="name" class="label">Quiz Name</label>
          <input
            id="name"
            v-model="name"
            type="text"
            class="input"
            placeholder="e.g. Midterm - Chapter 3"
          />

          <div class="row">
            <div class="field">
              <label for="start_date" class="label">Start Date</label>
              <input id="start_date" v-model="start_date" type="date" class="input" />
            </div>

            <div class="field">
              <label for="end_date" class="label">End Date</label>
              <input id="end_date" v-model="end_date" type="date" class="input" />
            </div>
          </div>

          <label for="time_duration" class="label">Duration (minutes)</label>
          <input
            id="time_duration"
            v-model.number="time_duration"
            type="number"
            class="input"
            min="1"
            placeholder="20"
          />

          <div class="actions">
            <button type="submit" class="btn-primary">Update</button>
            <router-link :to="`/admindash`" class="btn-secondary">Cancel</router-link>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "EditQuiz",
  data() {
    return {
      name: "",
      start_date: "",
      end_date: "",
      time_duration: null,
      chapterId: null
    };
  },
  created() {
    this.fetchQuiz();
  },
  methods: {
    async fetchQuiz() {
      try {
        const quizId = this.$route.params.quiz_id;
        const token = localStorage.getItem("token");
        const response = await axios.get(`http://localhost:5000/getquiz/${quizId}`, {
          headers: {
            "Accept": "application/json",
            Authorization: `Bearer ${token}`
          }
        });
        const quiz = Array.isArray(response.data.quizzes) ? response.data.quizzes[0] : response.data.quizzes;
        if (quiz) {
          this.name = quiz.name || "";
          this.start_date = quiz.start_date || "";
          this.end_date = quiz.end_date || "";
          this.time_duration = quiz.time_duration || null;
          this.chapterId = quiz.chapter_id || null;
        }
      } catch (error) {
        console.error("Error fetching quiz:", error);
      }
    },
    async updateQuiz() {
      try {
        const quizId = this.$route.params.quiz_id;
        const token = localStorage.getItem("token");
        const data = {
          name: this.name,
          start_date: this.start_date,
          end_date: this.end_date,
          time_duration: this.time_duration
        };
        const response = await axios.put(`http://localhost:5000/editquiz/${quizId}`, data, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          }
        });
        console.log("Quiz updated successfully:", response.data);
        this.$router.push(`/admindash`);
      } catch (error) {
        console.error("Error updating quiz:", error);
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
:root{
  --sidebar-bg: #1f2933;
  --accent: #0f4c5c;
  --muted: #6b7280;
  --card-bg: #ffffff;
  --radius: 12px;
  --gap: 16px;
  --max-width: 920px;
}

*{box-sizing:border-box}

.page{
  display:flex;
  min-height:100vh;
  background: linear-gradient(180deg,#f3f5f6,#e9ecef);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
  color:#0b1220;
}

.sidebar{
  width:220px;
  background:var(--sidebar-bg);
  padding:20px;
  display:flex;
  flex-direction:column;
  gap:12px;
  box-shadow:2px 0 8px rgba(2,6,23,0.08);
}

.nav-item{
  display:flex;
  gap:12px;
  align-items:center;
  color:#e6eef1;
  text-decoration:none;
  padding:10px 12px;
  border-radius:10px;
  font-weight:600;
  transition:background 120ms ease, transform 120ms ease;
}

.nav-item:hover{ background: rgba(255,255,255,0.04); transform: translateY(-2px); }
.nav-icon{ width:28px; text-align:center; font-size:1.05rem; }
.logout{ margin-top:auto; background: rgba(255,255,255,0.02); }

.main{
  flex:1;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  padding:28px;
  width:calc(100% - 240px);
}

.card{
  width:100%;
  max-width:var(--max-width);
  background:var(--card-bg);
  border-radius:var(--radius);
  padding:28px;
  box-shadow:0 8px 24px rgba(16,24,40,0.06);
  margin-top:72px;
}

.heading{
  margin:0 0 14px 0;
  font-size:1.4rem;
  color:#0b1220;
}

.form{
  display:flex;
  flex-direction:column;
  gap:12px;
}

.row{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:12px;
}

.field{ display:flex; flex-direction:column; gap:6px; }

.label{
  font-size:0.9rem;
  color:var(--muted);
  font-weight:600;
}

.input{
  height:44px;
  padding:0 12px;
  border-radius:10px;
  border:1px solid #d1d5db;
  background:#fbfdff;
  font-size:1rem;
  color:#0b1220;
  transition: box-shadow 120ms ease, border-color 120ms ease, transform 120ms ease;
  outline:none;
}

.input::placeholder{ color:#9ca3af; }
.input:focus{
  border-color:var(--accent);
  box-shadow:0 8px 20px rgba(15,76,92,0.06);
  transform: translateY(-1px);
}

.actions{
  display:flex;
  gap:12px;
  margin-top:6px;
  align-items:center;
}

.btn-primary{
  background: linear-gradient(180deg,var(--accent), #083b45);
  color:#fff;
  border:none;
  padding:10px 18px;
  border-radius:10px;
  font-weight:700;
  cursor:pointer;
}

.btn-secondary{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding:10px 14px;
  border-radius:10px;
  text-decoration:none;
  color:#0b1220;
  background:#f3f4f6;
  border:1px solid #e6e9eb;
  font-weight:600;
}

@media (max-width: 880px){
  .sidebar{ display:none; }
  .main{ width:100%; padding:18px; }
  .card{ margin-top:20px; padding:18px; }
  .row{ grid-template-columns: 1fr; }
}
</style>
