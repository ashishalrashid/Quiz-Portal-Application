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
        <div class="title-area">
          <h1 class="title">Quizzes</h1>
          <p class="subtitle">Manage quizzes for this chapter</p>
        </div>

        <div class="controls">
          <button @click="goToCreateQuiz" class="btn-primary">
            <i class="fas fa-plus-circle" aria-hidden="true"></i>
            <span>Add Quiz</span>
          </button>

          <div class="search">
            <input
              v-model="searchQuery"
              @keyup.enter="searchQuizzes"
              type="text"
              class="search-field"
              placeholder="Search quizzes..."
              aria-label="Search quizzes"
            />
            <button @click="searchQuizzes" class="search-btn" aria-label="Search">
              <i class="fas fa-search" aria-hidden="true"></i>
            </button>
          </div>
        </div>
      </header>

      <section class="table-wrap" aria-live="polite">
        <table class="quiz-table" role="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Chapter ID</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Duration</th>
              <th class="col-actions">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="!quizzes || quizzes.length === 0">
              <td colspan="7" class="empty">No quizzes found.</td>
            </tr>

            <tr v-for="quiz in quizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td class="cell-name">{{ quiz.name }}</td>
              <td>{{ quiz.chapter_id }}</td>
              <td>{{ quiz.start_date }}</td>
              <td>{{ quiz.end_date }}</td>
              <td>{{ quiz.time_duration }} minutes</td>
              <td class="action-buttons">
                <button @click="goToEditQuiz(quiz.id)" class="btn-ghost">Edit</button>
                <button @click="deleteQuiz(quiz.id)" class="btn-danger">Delete</button>
                <button @click="goToQuiz(quiz.id)" class="btn-primary small">Go To Quiz</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "Quizzes",
  data() {
    return {
      quizzes: [],
      searchQuery: ""
    };
  },
  created() {
    this.fetchQuizzes();
  },
  methods: {
    async fetchQuizzes() {
      try {
        const chapterId = this.$route.params.chapter_id;
        const response = await fetch(`http://localhost:5000/getquiz/${chapterId}`, {
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to fetch quizzes");
        }
        const data = await response.json();
        this.quizzes = data.quizzes;
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },
    async searchQuizzes() {
      try {
        const chapterId = this.$route.params.chapter_id;
        const response = await fetch(`http://localhost:5000/getsearchquiz/${chapterId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          },
          body: JSON.stringify({ pattern: this.searchQuery })
        });
        if (!response.ok) {
          throw new Error("Failed to search quizzes");
        }
        const data = await response.json();
        this.quizzes = data.quizzes;
      } catch (error) {
        console.error("Error searching quizzes:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToEditQuiz(quizId) {
      this.$router.push(`/editquiz/${quizId}`);
    },
    goToCreateQuiz() {
      const chapterId = this.$route.params.chapter_id;
      this.$router.push(`/createquiz/${chapterId}`);
    },
    goToQuiz(quizID) {
      this.$router.push(`/quiz/${quizID}`);
    },
    async deleteQuiz(quizId) {
      try {
        const response = await fetch(`http://localhost:5000/deletequiz/${quizId}`, {
          method: "DELETE",
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to delete quiz");
        }
        this.fetchQuizzes();
      } catch (error) {
        console.error("Error deleting quiz:", error);
      }
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

.title-area{ display:flex; flex-direction:column; }
.title{ margin:0; font-size:1.4rem; }
.subtitle{ margin:4px 0 0; color:var(--muted); font-size:0.95rem; }

.controls{ display:flex; gap:12px; align-items:center; }

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

.btn-primary.small{ padding:6px 10px; font-size:0.9rem; }

.search{ display:flex; gap:8px; align-items:center; }

.search-field{
  border-radius:10px;
  border:1px solid #e6e9eb;
  padding:8px 12px;
  min-width:180px;
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

.table-wrap{ background:var(--card-bg); border-radius:12px; padding:12px; box-shadow:0 8px 24px rgba(11,23,40,0.04); }

.quiz-table{
  width:100%;
  border-collapse:collapse;
  margin-top:8px;
  font-size:0.95rem;
}

.quiz-table thead th{
  text-align:left;
  padding:12px 14px;
  background:#f7fafb;
  color:#0b1220;
  font-weight:700;
  border-bottom:1px solid #eef2f6;
}

.quiz-table tbody td{
  padding:12px 14px;
  border-bottom:1px solid #f1f5f9;
  vertical-align:middle;
  color:#111827;
}

.quiz-table tbody tr:hover{ background:#fcfdff; }

.cell-name{ font-weight:700; color:#0b1220; }

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
  .quiz-table thead{ display:none; }
  .quiz-table, .quiz-table tbody, .quiz-table tr, .quiz-table td{ display:block; width:100%; }
  .quiz-table tr{ margin-bottom:14px; border-radius:8px; box-shadow:0 6px 18px rgba(11,23,40,0.04); background:#fff; padding:12px; }
  .quiz-table td{ padding:8px 10px; border:none; }
  .quiz-table td::before{ content: attr(data-label); display:block; font-weight:700; color:var(--muted); margin-bottom:6px; }
  .col-actions{ text-align:right; }
}
</style>
