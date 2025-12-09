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
      <header class="header">
        <div class="title-wrap">
          <h1 class="title">Questions</h1>
          <p class="subtitle">Manage questions for this quiz</p>
        </div>

        <div class="controls">
          <div class="search">
            <input
              v-model="searchQuery"
              @keyup.enter="searchQuestions"
              type="text"
              class="search-field"
              placeholder="Search questions..."
              aria-label="Search questions"
            />
            <button @click="searchQuestions" class="search-btn" aria-label="Search">
              <i class="fas fa-search" aria-hidden="true"></i>
            </button>
          </div>

          <button @click="goToCreateQuestion" class="btn-primary">
            <i class="fas fa-plus-circle" aria-hidden="true"></i>
            <span>Create Question</span>
          </button>
        </div>
      </header>

      <section class="table-wrap" aria-live="polite">
        <table class="question-table" role="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Question</th>
              <th>Options</th>
              <th>Answer</th>
              <th class="col-actions">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="!questions || questions.length === 0">
              <td colspan="5" class="empty">No questions found.</td>
            </tr>

            <tr v-for="question in questions" :key="question.id">
              <td class="cell-id">{{ question.id }}</td>
              <td class="cell-question">{{ question.question }}</td>
              <td class="cell-options">
                <ul class="options-list">
                  <li v-for="(option, index) in question.options" :key="index">{{ option }}</li>
                </ul>
              </td>
              <td class="cell-answer">{{ question.answer }}</td>
              <td class="action-buttons">
                <button @click="goToEditQuestion(question.id)" class="btn-ghost">Edit</button>
                <button @click="deleteQuestion(question.id)" class="btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Questions",
  data() {
    return {
      questions: [],
      searchQuery: ""
    };
  },
  created() {
    this.fetchQuestions();
  },
  methods: {
    async fetchQuestions() {
      try {
        const quizId = this.$route.params.quiz_id;
        const response = await fetch(`http://localhost:5000/getquestion/${quizId}`, {
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to fetch questions");
        }
        const data = await response.json();
        this.questions = data;
      } catch (error) {
        console.error("Error fetching questions:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToEditQuestion(questionId) {
      this.$router.push(`/question/${questionId}/edit`);
    },
    deleteQuestion(questionId) {
      axios
        .delete(`http://localhost:5000/deletequestion/${questionId}`, {
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        })
        .then(() => {
          this.fetchQuestions();
        })
        .catch(error => {
          console.error("Error deleting question:", error);
        });
    },
    async searchQuestions() {
      const quizId = this.$route.params.quiz_id;
      try {
        const response = await fetch(`http://localhost:5000/getsearchquestions/${quizId}`, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          },
          body: JSON.stringify({ pattern: this.searchQuery })
        });

        if (!response.ok) {
          throw new Error("Failed to search questions");
        }

        const data = await response.json();
        this.questions = data.questions;
      } catch (error) {
        console.error("Error searching questions:", error);
      }
    },
    goToCreateQuestion() {
      const quizId = this.$route.params.quiz_id;
      this.$router.push(`/createquestion/${quizId}`);
    }
  }
};
</script>

<style scoped>
:root{
  --sidebar-bg:#1f2933;
  --accent:#0f4c5c;
  --muted:#6b7280;
  --card-bg:#ffffff;
  --danger:#dc2626;
  --radius:12px;
  --max-width:1100px;
  --gap:16px;
}

*{box-sizing:border-box}

.page{
  display:flex;
  min-height:100vh;
  background:linear-gradient(180deg,#f3f5f6,#e9ecef);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial;
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
  transition:background 120ms,transform 120ms;
}

.nav-item:hover{ background:rgba(255,255,255,0.04); transform:translateY(-2px); }
.nav-icon{ width:28px; text-align:center; font-size:1.05rem; }
.logout{ margin-top:auto; background:rgba(255,255,255,0.02); }

.main{
  flex:1;
  padding:28px;
  max-width:var(--max-width);
  margin:0 auto;
  width:calc(100% - 260px);
}

.header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  margin-bottom:18px;
}

.title-wrap{ display:flex; flex-direction:column; }
.title{ margin:0; font-size:1.4rem; }
.subtitle{ margin:4px 0 0; color:var(--muted); font-size:0.95rem; }

.controls{ display:flex; gap:12px; align-items:center; }

.search{ display:flex; gap:8px; align-items:center; }

.search-field{
  border-radius:10px;
  border:1px solid #e6e9eb;
  padding:8px 12px;
  min-width:220px;
  outline:none;
}

.search-btn{
  border-radius:10px;
  border:none;
  padding:8px 10px;
  color:#fff;
  background:var(--accent);
  cursor:pointer;
}

.btn-primary{
  display:inline-flex;
  gap:8px;
  align-items:center;
  background:linear-gradient(180deg,var(--accent),#083b45);
  color:#fff;
  border:none;
  padding:10px 14px;
  border-radius:10px;
  cursor:pointer;
  font-weight:700;
}

.table-wrap{ background:var(--card-bg); border-radius:12px; padding:12px; box-shadow:0 8px 24px rgba(11,23,40,0.04); }

.question-table{
  width:100%;
  border-collapse:collapse;
  margin-top:8px;
  font-size:0.95rem;
}

.question-table thead th{
  text-align:left;
  padding:12px 14px;
  background:#f7fafb;
  color:#0b1220;
  font-weight:700;
  border-bottom:1px solid #eef2f6;
}

.question-table tbody td{
  padding:12px 14px;
  border-bottom:1px solid #f1f5f9;
  vertical-align:middle;
  color:#111827;
}

.options-list{ padding-left: 18px; margin: 0; }
.options-list li{ margin-bottom: 6px; color:var(--muted); }

.cell-question{ max-width:420px; word-break:break-word; }
.cell-options{ max-width:320px; }

.question-table tbody tr:hover{ background:#fcfdff; }

.action-buttons{ display:flex; gap:8px; align-items:center; }

.btn-ghost{
  background:transparent;
  border:1px solid rgba(15,76,92,0.08);
  padding:8px 10px;
  border-radius:8px;
  color:var(--accent);
  cursor:pointer;
  font-weight:700;
}

.btn-danger{
  background:var(--danger);
  color:white;
  padding:8px 10px;
  border:none;
  border-radius:8px;
  cursor:pointer;
  font-weight:700;
}

.empty{ text-align:center; padding:22px; color:var(--muted); }

@media (max-width:960px){
  .sidebar{ display:none; }
  .main{ width:100%; padding:18px; }
  .question-table thead{ display:none; }
  .question-table, .question-table tbody, .question-table tr, .question-table td{ display:block; width:100%; }
  .question-table tr{ margin-bottom:14px; border-radius:8px; box-shadow:0 6px 18px rgba(11,23,40,0.04); background:#fff; padding:12px; }
  .question-table td{ padding:8px 10px; border:none; }
  .question-table td::before{ content: attr(data-label); display:block; font-weight:700; color:var(--muted); margin-bottom:6px; }
  .col-actions{ text-align:right; }
}
</style>
