<template>
  <div class="page">
    <aside class="sidebar" aria-label="User navigation">
      <router-link to="/userdash" class="nav-item disabled" title="Home">
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
      <header class="hero">
        <h1 class="hero-title">Your Subjects</h1>
        <p class="hero-sub">Quick access to subjects you're enrolled in</p>
      </header>

      <section class="grid" aria-live="polite">
        <ul class="list" v-if="subjects && subjects.length">
          <li
            v-for="subject in subjects"
            :key="subject.id"
            class="card"
            @click="goToSubject(subject.id)"
            role="button"
            tabindex="0"
            @keyup.enter="goToSubject(subject.id)"
            :aria-label="`Open subject ${subject.name}`"
          >
            <div class="card-body">
              <h3 class="card-title">{{ subject.name }}</h3>
              <p class="card-desc">{{ subject.description || 'No description' }}</p>
            </div>
            <div class="card-meta">
              <span class="chip">Chapters: {{ subject.chapter_count ?? '—' }}</span>
              <span class="chip">Quizzes: {{ subject.quiz_count ?? '—' }}</span>
            </div>
          </li>
        </ul>

        <div v-else class="empty">
          No subjects available.
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "SubjectList",
  data() {
    return {
      subjects: []
    };
  },
  methods: {
    async fetchSubjects() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5000/getus", {
          headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${token}`
          }
        });
        const data = await response.json();
        this.subjects = data.subjects;
      } catch (error) {
        console.error("Error fetching subjects:", error);
      }
    },
    goToSubject(subjectId) {
      this.$router.push(`/usubject/${subjectId}`);
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  },
  mounted() {
    this.fetchSubjects();
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
  --gap:16px;
  --max-width:1100px;
}

*{box-sizing:border-box}

.page{
  display:flex;
  min-height:100vh;
  background:linear-gradient(180deg,#f3f5f6,#e9ecef);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
  color:#0b1220;
}

.sidebar{
  width:220px;
  background:var(--sidebar-bg);
  padding:18px;
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

.nav-item:hover{ background:rgba(255,255,255,0.04); transform:translateY(-2px); }
.nav-icon{ width:28px; text-align:center; font-size:1.05rem; }
.disabled{ background:rgba(255,255,255,0.03); cursor:default; }
.logout{ margin-top:auto; background:rgba(255,255,255,0.02); }

.main{
  flex:1;
  padding:28px;
  max-width:var(--max-width);
  margin:0 auto;
  width:calc(100% - 260px);
}

.hero{
  margin-bottom:18px;
}

.hero-title{
  margin:0;
  font-size:1.4rem;
  font-weight:700;
}

.hero-sub{
  margin:6px 0 0 0;
  color:var(--muted);
  font-size:0.95rem;
}

.grid{ display:block; }

.list{
  display:flex;
  flex-wrap:wrap;
  gap:16px;
  list-style:none;
  padding:0;
  margin:0;
}

.card{
  width:320px;
  background:var(--card-bg);
  border-radius:10px;
  border:1px solid #e6e9eb;
  box-shadow:0 8px 20px rgba(11,23,40,0.04);
  display:flex;
  flex-direction:column;
  cursor:pointer;
  transition:transform 120ms ease, box-shadow 120ms ease;
}

.card:hover{ transform:translateY(-6px); box-shadow:0 14px 36px rgba(11,23,40,0.08); }

.card-body{
  padding:18px;
  flex:1;
}

.card-title{ font-size:1.1rem; font-weight:700; margin:0 0 8px 0; }
.card-desc{ color:var(--muted); margin:0; min-height:48px; }

.card-meta{
  display:flex;
  gap:8px;
  padding:12px 16px;
  border-top:1px solid #f1f4f6;
  align-items:center;
}

.chip{
  background:#f3f4f6;
  color:#0b1220;
  padding:6px 10px;
  border-radius:999px;
  font-weight:600;
  font-size:0.85rem;
}

.empty{
  padding:40px;
  color:var(--muted);
  text-align:center;
}

@media (max-width:980px){
  .sidebar{ display:none; }
  .main{ width:100%; padding:18px; }
  .list{ justify-content:center; }
  .card{ width:100%; max-width:520px; }
}
</style>
