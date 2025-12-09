<template>
  <div class="page">
    <aside class="sidebar">
      <router-link to="/admindash" class="nav-item disabled">
        <i class="fas fa-home nav-icon"></i>
        <span class="nav-label">Home</span>
      </router-link>

      <router-link to="/admindash/subjects" class="nav-item">
        <i class="fas fa-book nav-icon"></i>
        <span class="nav-label">Subjects</span>
      </router-link>

      <router-link to="/admindash/user" class="nav-item">
        <i class="fas fa-user nav-icon"></i>
        <span class="nav-label">Users</span>
      </router-link>

      <router-link to="/admindash/stats" class="nav-item">
        <i class="fas fa-chart-bar nav-icon"></i>
        <span class="nav-label">Stats</span>
      </router-link>

      <a href="#" @click.prevent="logout" class="nav-item logout">
        <i class="fas fa-sign-out-alt nav-icon"></i>
        <span class="nav-label">Log Out</span>
      </a>
    </aside>
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
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) throw new Error();
        const data = await response.json();
        this.subjects = data.subjects;
      } catch (e) {}
    },
    async fetchCounts() {
      try {
        const response = await fetch("http://localhost:5000/getcounts", {
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) throw new Error();
        const data = await response.json();
        this.counts = data;
      } catch (e) {}
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToSubject(id) {
      this.$router.push(`/admindash/subject/${id}`);
    },
    goToAddChapter(id) {
      this.$router.push(`/admindash/subject/${id}/addchapter`);
    },
    goToAllSubjects() {
      this.$router.push("/admindash/subjects");
    }
  }
};
</script>

<style scoped>
:root {
  --sidebar-bg: #1f2933;
  --accent: #0f4c5c;
  --text-light: #e6eef1;
  --radius: 12px;
}

.page {
  display: flex;
  width: 100%;
  min-height: 100vh;
  background: #f3f4f6;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
}

.sidebar {
  width: 240px;
  background: var(--sidebar-bg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-light);
  text-decoration: none;
  padding: 12px;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  transition: background 120ms ease, transform 120ms ease;
}

.nav-item:hover {
  background: rgba(255,255,255,0.06);
  transform: translateY(-2px);
}

.nav-icon {
  font-size: 1.1rem;
  width: 26px;
  text-align: center;
}

.disabled {
  background: rgba(255,255,255,0.1);
  cursor: default;
}

.logout {
  margin-top: auto;
  background: rgba(255,255,255,0.05);
}

.logout:hover {
  background: rgba(255,255,255,0.12);
}

@media (max-width: 900px) {
  .sidebar {
    width: 70px;
    padding: 14px 8px;
  }
  .nav-label {
    display: none;
  }
}
</style>
