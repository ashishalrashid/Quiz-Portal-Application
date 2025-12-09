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

      <router-link to="/admindash/stats" class="nav-item disabled" title="Stats">
        <i class="fas fa-chart-bar nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Stats</span>
      </router-link>

      <a href="#" @click.prevent="logout" class="nav-item logout" role="button" title="Log out">
        <i class="fas fa-sign-out-alt nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Log Out</span>
      </a>
    </aside>

    <main class="main" role="main">
      <section class="card" aria-labelledby="stats-heading">
        <header class="card-header">
          <h2 id="stats-heading" class="heading">Subject Statistics</h2>
        </header>

        <div class="chart-wrap">
          <canvas id="subjectChart" ref="subjectChart" aria-label="Subject statistics chart"></canvas>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: "SubjectStats",
  data() {
    return {
      stats: [],
      chartInstance: null
    };
  },
  async created() {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/subjectstats", {
        headers: {
          Accept: "application/json",
          Authorization: "Bearer " + token
        }
      });
      const data = await response.json();
      this.stats = data.stats || [];
      this.$nextTick(() => this.renderChart());
    } catch (error) {
      console.error("Error fetching subject statistics:", error);
    }
  },
  methods: {
    renderChart() {
      if (this.chartInstance) {
        this.chartInstance.destroy();
        this.chartInstance = null;
      }
      const canvas = this.$refs.subjectChart;
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      const labels = this.stats.map(s => s.name);
      const userCounts = this.stats.map(s => Number(s.user_count || 0));
      const avgScores = this.stats.map(s => (s.avg_score ? parseFloat(s.avg_score) : 0));
      this.chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "User Count",
              data: userCounts,
              backgroundColor: "rgba(16, 185, 129, 0.18)",
              borderColor: "rgba(16, 185, 129, 1)",
              borderWidth: 1
            },
            {
              label: "Average Score",
              data: avgScores,
              backgroundColor: "rgba(99, 102, 241, 0.16)",
              borderColor: "rgba(99, 102, 241, 1)",
              borderWidth: 1,
              yAxisID: "scoreAxis"
            }
          ]
        },
        options: {
          responsive: true,
          interaction: { mode: "index", intersect: false },
          scales: {
            y: {
              beginAtZero: true,
              position: "left",
              title: { display: true, text: "Users" }
            },
            scoreAxis: {
              beginAtZero: true,
              position: "right",
              grid: { drawOnChartArea: false },
              title: { display: true, text: "Avg Score" }
            }
          },
          plugins: {
            legend: { position: "top" },
            tooltip: { enabled: true }
          }
        }
      });
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  },
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
      this.chartInstance = null;
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
  --max-width: 1100px;
  --gap: 18px;
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
.nav-icon { width: 28px; text-align:center; font-size:1.05rem; }
.disabled { background: rgba(255,255,255,0.03); cursor: default; }
.logout { margin-top: auto; background: rgba(255,255,255,0.02); }

.main {
  flex: 1;
  padding: 28px;
  display: flex;
  justify-content: center;
}

.card {
  width: 100%;
  max-width: var(--max-width);
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: 0 10px 30px rgba(11,23,40,0.06);
}

.card-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.heading { margin:0; font-size:1.4rem; }

.chart-wrap { width: 100%; height: 420px; display:flex; align-items:stretch; }
canvas { width: 100% !important; height: 100% !important; }

@media (max-width: 980px) {
  .sidebar { display: none; }
  .main { padding: 18px; }
  .chart-wrap { height: 320px; }
}
</style>
