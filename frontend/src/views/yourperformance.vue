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

      <router-link to="/yourperformance" class="nav-item disabled" title="Your Performance">
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
        <div>
          <h1 class="title">Your Performance</h1>
          <p class="subtitle">Summary of your quiz scores</p>
        </div>
      </header>

      <section class="card">
        <div class="table-wrap" aria-live="polite">
          <table class="performance-table" role="table">
            <thead>
              <tr>
                <th scope="col">Subject</th>
                <th scope="col">Chapter</th>
                <th scope="col">Quiz</th>
                <th scope="col">Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!performance || performance.length === 0">
                <td colspan="4" class="empty">No performance data available.</td>
              </tr>

              <tr v-for="item in performance" :key="item.quiz_name + item.subject_name">
                <td class="cell-subject">{{ item.subject_name || "—" }}</td>
                <td class="cell-chapter">{{ item.chapter_name || "—" }}</td>
                <td class="cell-quiz">{{ item.quiz_name || "—" }}</td>
                <td class="cell-score">{{ item.score != null ? item.score : "—" }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "YourPerformance",
  data() {
    return {
      performance: []
    };
  },
  created() {
    this.fetchPerformance();
  },
  methods: {
    async fetchPerformance() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:5000/yourperformance", {
          headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${token}`
          }
        });
        this.performance = response.data.performance;
      } catch (error) {
        console.error("Error fetching performance:", error);
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
  --sidebar-bg:#0f1724;
  --accent:#0f4c5c;
  --muted:#6b7280;
  --card-bg:#ffffff;
  --radius:12px;
  --max-width:1100px;
}

* { box-sizing: border-box; }

.page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(180deg,#f7fafc,#eef2f6);
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial;
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
.disabled { background: rgba(255,255,255,0.03); cursor: default; }
.logout { margin-top: auto; background: rgba(255,255,255,0.02); }

.main {
  flex: 1;
  padding: 28px;
  max-width: var(--max-width);
  margin: 0 auto;
  width: calc(100% - 260px);
}

.header {
  margin-bottom: 18px;
}

.title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 700;
}

.subtitle {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 0.95rem;
}

.card {
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: 0 8px 24px rgba(11,23,40,0.06);
}

.table-wrap { overflow: auto; }

.performance-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.performance-table thead th {
  text-align: left;
  padding: 12px 14px;
  background: #fbfdff;
  color: #0b1220;
  font-weight: 700;
  border-bottom: 1px solid #eef2f6;
}

.performance-table tbody td {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
  color: #111827;
}

.performance-table tbody tr:hover {
  background: #fcfeff;
}

.cell-subject { font-weight: 700; color: #0b1220; }
.cell-score { font-weight: 700; color: var(--accent); }

.empty {
  text-align: center;
  padding: 24px;
  color: var(--muted);
}

@media (max-width: 980px) {
  .sidebar { display: none; }
  .main { width: 100%; padding: 18px; }
  .performance-table thead { display: none; }
  .performance-table, .performance-table tbody, .performance-table tr, .performance-table td {
    display: block;
    width: 100%;
  }
  .performance-table tr {
    margin-bottom: 14px;
    border-radius: 8px;
    background: #fff;
    box-shadow: 0 6px 18px rgba(11,23,40,0.04);
    padding: 12px;
  }
  .performance-table td { padding: 8px 10px; border: none; }
  .performance-table td::before {
    content: attr(data-label);
    display: block;
    font-weight: 700;
    color: var(--muted);
    margin-bottom: 6px;
  }
}
</style>
