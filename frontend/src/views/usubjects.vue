<template>
  <div class="page">
    <aside class="sidebar" aria-label="User navigation">
      <router-link to="/userdash" class="nav-item" title="Home">
        <i class="fas fa-home nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Home</span>
      </router-link>

      <router-link to="/uallsubjects" class="nav-item" title="All Subjects">
        <i class="fas fa-book nav-icon" aria-hidden="true"></i>
        <span class="nav-label">All Subjects</span>
      </router-link>

      <router-link to="/yourperformance" class="nav-item" title="Your Performance">
        <i class="fas fa-chart-bar nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Your Performance</span>
      </router-link>

      <a href="#" @click.prevent="logout" class="nav-item logout" role="button" title="Log out">
        <i class="fas fa-sign-out-alt nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Log Out</span>
      </a>
    </aside>

    <main class="main" role="main">
      <header class="header">
        <div class="title-area">
          <h1 class="title">Active Quizzes</h1>
          <p class="subtitle">Take quizzes assigned to this subject</p>
        </div>

        <div class="controls">
          <div class="search">
            <input
              v-model="searchQuery"
              type="text"
              class="search-field"
              placeholder="Search quizzes..."
              @keyup.enter="searchQuizzes"
              aria-label="Search quizzes"
            />
            <button @click="searchQuizzes" class="search-btn" aria-label="Search quizzes">
              <i class="fas fa-search" aria-hidden="true"></i>
            </button>
          </div>
        </div>
      </header>

      <section class="table-wrap" aria-live="polite">
        <table class="quiz-table" role="table">
          <thead>
            <tr>
              <th scope="col">Quiz Name</th>
              <th scope="col">Chapter</th>
              <th scope="col">Start Date</th>
              <th scope="col">End Date</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="!quizzes || quizzes.length === 0">
              <td colspan="5" class="empty">No active quizzes found.</td>
            </tr>

            <tr v-for="quiz in quizzes" :key="quiz.id">
              <td class="cell-name">{{ quiz.quiz_name }}</td>
              <td>{{ quiz.chapter_name }}</td>
              <td>{{ quiz.start_date }}</td>
              <td>{{ quiz.end_date }}</td>
              <td>
                <button @click="goToQuiz(quiz.id)" class="btn-primary" aria-label="Take quiz">
                  Go To Quiz
                </button>
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
  name: "ActiveQuizzes",
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
        const token = localStorage.getItem("token");
        const subjectId = this.$route.params.subject_id;
        const response = await fetch(`http://localhost:5000/getuserquizzes/${subjectId}`, {
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + token
          }
        });
        if (!response.ok) {
          throw new Error("Failed to fetch active quizzes");
        }
        const data = await response.json();
        this.quizzes = data.quizzes;
      } catch (error) {
        console.error("Error fetching active quizzes:", error);
      }
    },
    async searchQuizzes() {
      try {
        const token = localStorage.getItem("token");
        const subjectId = this.$route.params.subject_id;
        const response = await fetch(`http://localhost:5000/searchuserquizzes/${subjectId}`, {
          method: "POST",
          headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({ pattern: this.searchQuery })
        });

        if (!response.ok) {
          throw new Error("Failed to fetch quizzes");
        }

        const data = await response.json();
        this.quizzes = data.quizzes;
      } catch (error) {
        console.error("Error searching quizzes:", error);
      }
    },
    goToQuiz(quizId) {
      this.$router.push(`/takequiz/${quizId}`);
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
  --sidebar-bg: #0f1724;
  --accent: #0f4c5c;
  --muted: #6b7280;
  --card-bg: #ffffff;
  --radius: 12px;
  --gap: 16px;
  --max-width: 1100px;
}

* { box-sizing: border-box; }

.page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(180deg,#f3f5f6,#e9ecef);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
  color: #0b1220;
}

.sidebar {
  width: 220px;
  background: var(--sidebar-bg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 2px 0 8px rgba(2,6,23,0.08);
}

.nav-item {
  display: flex;
  gap: 12px;
  align-items: center;
  color: #e6eef1;
  text-decoration: none;
  padding: 10px 12px;
  border-radius: 10px;
  font-weight: 600;
  transition: background 120ms ease, transform 120ms ease;
}

.nav-item:hover { background: rgba(255,255,255,0.04); transform: translateY(-2px); }
.nav-icon { width: 28px; text-align: center; font-size: 1.05rem; }
.logout { margin-top: auto; background: rgba(255,255,255,0.02); }

.main {
  flex: 1;
  padding: 28px;
  max-width: var(--max-width);
  margin: 0 auto;
  width: calc(100% - 260px);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.title-area { display: flex; flex-direction: column; }
.title { margin: 0; font-size: 1.4rem; }
.subtitle { margin: 4px 0 0; color: var(--muted); font-size: 0.95rem; }

.controls { display: flex; gap: 12px; align-items: center; }

.search { display: flex; gap: 8px; align-items: center; }
.search-field {
  border-radius: 10px;
  border: 1px solid #e6e9eb;
  padding: 10px 12px;
  min-width: 220px;
  outline: none;
}
.search-field:focus { box-shadow: 0 8px 20px rgba(15,76,92,0.06); border-color: var(--accent); }

.search-btn {
  border-radius: 10px;
  border: none;
  padding: 10px 12px;
  color: #fff;
  background: var(--accent);
  cursor: pointer;
}

.table-wrap { background: var(--card-bg); border-radius: 12px; padding: 12px; box-shadow: 0 8px 24px rgba(11,23,40,0.04); }

.quiz-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
  font-size: 0.95rem;
}

.quiz-table thead th {
  text-align: left;
  padding: 12px 14px;
  background: #f7fafb;
  color: #0b1220;
  font-weight: 700;
  border-bottom: 1px solid #eef2f6;
}

.quiz-table tbody td {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
  color: #111827;
}

.quiz-table tbody tr:hover {
  background: #fcfdff;
}

.empty {
  text-align: center;
  padding: 22px;
  color: var(--muted);
}

.btn-primary {
  background: linear-gradient(180deg,var(--accent), #083b45);
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
}

.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(11,23,40,0.08); }

.cell-name { font-weight: 700; color: #0b1220; }

@media (max-width: 900px) {
  .sidebar { display: none; }
  .main { width: 100%; padding: 16px; }
  .search-field { min-width: 120px; }
  .quiz-table thead { display: none; }
  .quiz-table, .quiz-table tbody, .quiz-table tr, .quiz-table td {
    display: block;
    width: 100%;
  }
  .quiz-table tr { margin-bottom: 14px; border-radius: 8px; box-shadow: 0 6px 18px rgba(11,23,40,0.04); background: #fff; padding: 12px; }
  .quiz-table td { padding: 8px 10px; border: none; }
  .quiz-table td::before {
    content: attr(data-label);
    font-weight: 700;
    display: block;
    margin-bottom: 6px;
    color: var(--muted);
  }
  .quiz-table td:last-child { display: flex; justify-content: flex-end; }
}
</style>
