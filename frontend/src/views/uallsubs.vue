<template>
  <div class="page">
    <aside class="sidebar" aria-label="User navigation">
      <router-link to="/userdash" class="nav-item" title="Home">
        <i class="fas fa-home nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Home</span>
      </router-link>

      <router-link to="/uallsubjects" class="nav-item disabled" title="All Subjects">
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
        <h1 class="title">All Subjects</h1>

        <div class="controls">
          <div class="search">
            <input v-model="searchQuery" type="text" class="search-field" placeholder="Search subjects..." />
            <button @click="searchOtherSubjects" class="search-btn" aria-label="Search">
              <i class="fas fa-search" aria-hidden="true"></i>
            </button>
          </div>
        </div>
      </header>

      <section class="grid" aria-live="polite">
        <ul class="list" v-if="subjects && subjects.length">
          <li v-for="subject in subjects" :key="subject.id" class="card" role="group">
            <div
              class="card-body"
              @click="goToSubject(subject.id)"
              role="button"
              tabindex="0"
              @keyup.enter="goToSubject(subject.id)"
              :aria-label="`Open subject ${subject.name}`"
            >
              <h3 class="card-title">{{ subject.name }}</h3>
              <p class="card-desc">{{ subject.description || 'No description' }}</p>
            </div>

            <div class="card-actions">
              <button class="btn-primary" @click.stop="SubscribeSubject(subject.id)">Subscribe</button>
            </div>
          </li>
        </ul>

        <div v-else class="empty">
          No subjects found.
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "UAllSubjects",
  data() {
    return {
      subjects: [],
      searchQuery: ""
    };
  },
  created() {
    this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await fetch("http://localhost:5000/getothersubjects", {
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) throw new Error("Failed to fetch subjects");
        const data = await response.json();
        this.subjects = data.subjects || [];
      } catch (error) {
        console.error("Error fetching subjects:", error);
      }
    },
    async searchOtherSubjects() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5000/getsearchothersubjects", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ pattern: this.searchQuery })
        });
        if (!response.ok) throw new Error("Failed to fetch subjects");
        const data = await response.json();
        this.subjects = data.subjects || [];
      } catch (error) {
        console.error("Error searching subjects:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToSubject(subjectId) {
      this.$router.push(`/subject/${subjectId}`);
    },
    async SubscribeSubject(subjectId) {
      try {
        const response = await fetch(`http://localhost:5000/createusersubject/${subjectId}`, {
          method: "POST",
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) throw new Error("Failed to subscribe subject");
        alert("Subscribed!");
        this.fetchSubjects();
      } catch (error) {
        console.error("Error subscribing subject:", error);
      }
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
  --gap:16px;
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
.disabled{ background:rgba(255,255,255,0.03); cursor:default; }
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

.title{ margin:0; font-size:1.4rem; }

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
  width:240px;
  background:var(--card-bg);
  border-radius:10px;
  border:1px solid #e6e9eb;
  box-shadow:0 8px 20px rgba(11,23,40,0.04);
  display:flex;
  flex-direction:column;
  min-height:220px;
  transition:transform 120ms,box-shadow 120ms;
}

.card:hover{ transform:translateY(-6px); box-shadow:0 14px 36px rgba(11,23,40,0.08); }

.card-body{
  padding:16px;
  cursor:pointer;
  flex:1;
  display:flex;
  flex-direction:column;
  gap:8px;
}

.card-title{ font-size:1.05rem; font-weight:700; margin:0; }
.card-desc{ color:var(--muted); font-size:0.92rem; margin:0; min-height:48px; }

.card-actions{
  padding:12px;
  display:flex;
  gap:8px;
  justify-content:center;
  border-top:1px solid #f1f4f6;
  border-bottom-left-radius:10px;
  border-bottom-right-radius:10px;
}

.btn-primary{
  display:inline-flex;
  align-items:center;
  gap:8px;
  background:linear-gradient(180deg,var(--accent),#083b45);
  color:#fff;
  border:none;
  padding:8px 12px;
  border-radius:8px;
  cursor:pointer;
  font-weight:700;
}

.btn-primary:hover{ transform:translateY(-2px); }

.empty{ padding:36px; color:var(--muted); text-align:center; }

@media (max-width:980px){
  .sidebar{ display:none; }
  .main{ width:100%; padding:18px; }
  .list{ justify-content:center; }
  .search-field{ min-width:140px; }
}
</style>
