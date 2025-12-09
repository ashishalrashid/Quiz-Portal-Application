<template>
  <div class="page">
    <aside class="sidebar" aria-label="Admin dashboard navigation">
      <router-link to="/admindash" class="nav-item disabled" title="Home (current)">
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
      <section class="content" aria-labelledby="dashboard-heading">
        <header class="content-header">
          <h1 id="dashboard-heading" class="title">Dashboard</h1>
          <div class="header-actions">
            <router-link to="/admindash/subjects" class="btn-outline" @click.prevent="goToAllSubjects">All Subjects</router-link>
          </div>
        </header>

        <div class="layout">
          <div class="panel subjects-panel" aria-labelledby="subjects-heading">
            <div class="panel-header">
              <h2 id="subjects-heading" class="panel-title">Subjects</h2>
              <small class="panel-sub">Showing up to 4 recent subjects</small>
            </div>

            <ul class="subjects-list" v-if="subjects && subjects.length">
              <li
                v-for="subject in subjects.slice(0, 4)"
                :key="subject.id"
                class="subject-card"
                @click="goToSubject(subject.id)"
                role="button"
                :aria-label="`Open subject ${subject.name}`"
                tabindex="0"
                @keyup.enter="goToSubject(subject.id)"
              >
                <div class="subject-title">{{ subject.name }}</div>
                <div class="subject-desc">{{ subject.description || 'No description' }}</div>
                <div class="subject-actions">
                  <button class="link-btn" @click.stop="goToAddChapter(subject.id)">Add Chapter</button>
                  <router-link :to="`/admindash/subject/${subject.id}`" class="link-btn" @click.native.stop>Open</router-link>
                </div>
              </li>
            </ul>

            <div v-else class="empty">
              No subjects found.
            </div>
          </div>

          <aside class="panel stats-panel" aria-labelledby="stats-heading">
            <div class="panel-header">
              <h2 id="stats-heading" class="panel-title">Statistics</h2>
            </div>

            <ul class="stats-list">
              <li class="stat-card">
                <div class="stat-label">User Count</div>
                <div class="stat-number">{{ counts.user_count }}</div>
              </li>
              <li class="stat-card">
                <div class="stat-label">Quiz Count</div>
                <div class="stat-number">{{ counts.quiz_count }}</div>
              </li>
              <li class="stat-card">
                <div class="stat-label">Subject Count</div>
                <div class="stat-number">{{ counts.subject_count }}</div>
              </li>
              <li class="stat-card">
                <div class="stat-label">Chapter Count</div>
                <div class="stat-number">{{ counts.chapter_count }}</div>
              </li>
            </ul>
          </aside>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      subjects: [],
      counts: {
        user_count: 0,
        quiz_count: 0,
        subject_count: 0,
        chapter_count: 0
      }
    };
  },
  created() {
    this.fetchSubjects();
    this.fetchCounts();
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await fetch("http://localhost:5000/getsubjects", {
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to fetch subjects");
        }
        const data = await response.json();
        this.subjects = data.subjects;
      } catch (error) {
        console.error("Error fetching subjects:", error);
      }
    },
    async fetchCounts() {
      try {
        const response = await fetch("http://localhost:5000/getcounts", {
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to fetch counts");
        }
        const data = await response.json();
        this.counts = data;
      } catch (error) {
        console.error("Error fetching counts:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToSubject(subjectId) {
      this.$router.push(`/admindash/subject/${subjectId}`);
    },
    goToAddChapter(subjectId) {
      this.$router.push(`/admindash/subject/${subjectId}/addchapter`);
    },
    goToAllSubjects() {
      this.$router.push("/admindash/subjects");
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
  --max-width: 1100px;
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
}
.nav-item .nav-icon {
  width: 28px;
  text-align: center;
  font-size: 1.05rem;
}
.nav-item .nav-label { display: inline-block; }
.nav-item:hover, .nav-item:focus { background: rgba(255,255,255,0.04); transform: translateY(-2px); outline: none; }
.disabled { background: rgba(255,255,255,0.03); cursor: default; }
.logout { margin-top: auto; background: rgba(255,255,255,0.02); }

/* Main */
.main { flex: 1; display: flex; justify-content: center; padding: var(--container-padding); }
.content { width: 100%; max-width: var(--max-width); }

/* Header */
.content-header { display:flex; justify-content: space-between; align-items:center; gap:12px; margin-bottom: 18px; }
.title { margin:0; font-size:1.5rem; }
.header-actions .btn-outline { text-decoration:none; padding:8px 12px; border-radius:8px; background:#f3f4f6; color:#0b1220; border:1px solid #e6e9eb; font-weight:600; }

/* layout */
.layout { display: grid; grid-template-columns: 1fr 320px; gap: 20px; align-items: start; }

/* Subjects panel */
.panel { background: var(--card-bg); border-radius: var(--radius); padding: 18px; box-shadow: 0 6px 18px rgba(16,24,40,0.04); }
.panel-header { margin-bottom: 12px; display:flex; align-items:baseline; gap:8px; }
.panel-title { margin:0; font-size:1.1rem; }
.panel-sub { color: var(--muted); font-size:0.9rem; }

/* Subject cards */
.subjects-list { display:flex; gap:12px; padding:0; margin:0; list-style:none; flex-wrap:wrap; }
.subject-card {
  background: linear-gradient(180deg,#ffffff,#fbfdff);
  border-radius: 10px;
  border: 1px solid #e6e9eb;
  padding: 12px;
  width: 220px;
  cursor: pointer;
  display:flex;
  flex-direction:column;
  gap:8px;
  transition: transform 120ms ease, box-shadow 120ms ease;
}
.subject-card:focus { outline: none; box-shadow: 0 6px 18px rgba(15,76,92,0.08); transform: translateY(-4px); }
.subject-card:hover { transform: translateY(-4px); box-shadow: 0 10px 26px rgba(11,23,40,0.06); }
.subject-title { font-weight:700; font-size:1rem; color:#0b1220; }
.subject-desc { color: var(--muted); font-size:0.9rem; min-height:40px; }
.subject-actions { display:flex; gap:8px; margin-top:auto; }
.link-btn { background:none; border:none; color:var(--accent); padding:6px 8px; cursor:pointer; font-weight:600; text-decoration:underline; border-radius:6px; }
.link-btn:hover { background: rgba(15,76,92,0.05); }

/* Empty state */
.empty { color: var(--muted); padding: 18px; }

/* Stats panel */
.stats-list { display:flex; flex-direction:column; gap:12px; list-style:none; padding:0; margin:0; }
.stat-card { background: linear-gradient(180deg,#ffffff,#fbfdff); padding:12px; border-radius:10px; border:1px solid #e6e9eb; display:flex; justify-content:space-between; align-items:center; }
.stat-label { color: var(--muted); font-weight:600; }
.stat-number { font-size:1.4rem; font-weight:800; color:var(--accent); }

/* Responsive */
@media (max-width: 980px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { display:none; }
  .content-header { flex-direction: column; align-items:flex-start; gap:8px; }
}
</style>
