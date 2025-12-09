<template>
  <div class="page">
    <aside class="sidebar" aria-label="Admin navigation">
      <router-link to="/admindash" class="nav-item" title="Home">
        <i class="fas fa-home nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Home</span>
      </router-link>

      <router-link to="/admindash/subjects" class="nav-item disabled" title="Subjects">
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
        <h1 class="title">Subjects</h1>
        <div class="controls">
          <router-link :to="`/admindash/createsubject`" class="btn-primary">
            <i class="fas fa-plus-circle" aria-hidden="true"></i>
            <span>Add Subject</span>
          </router-link>

          <div class="search">
            <input v-model="searchQuery" type="text" class="search-field" placeholder="Search..." />
            <button @click="searchSubjects" class="search-btn" aria-label="Search">
              <i class="fas fa-search" aria-hidden="true"></i>
            </button>
          </div>
        </div>
      </header>

      <section class="grid">
        <ul class="list" aria-live="polite">
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
              <button class="btn-ghost" @click.stop="goToEditSubject(subject.id)">Edit</button>
              <button class="btn-danger" @click.stop="deleteSubject(subject.id)">Delete</button>
            </div>
          </li>
        </ul>

        <div v-if="!subjects || subjects.length === 0" class="empty">No subjects available.</div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "Subjects",
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
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToSubject(subjectId) {
      this.$router.push(`/admindash/subject/${subjectId}`);
    },
    goToEditSubject(subjectId) {
      this.$router.push(`/editsubject/${subjectId}`);
    },
    async searchSubjects() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5000/getsearchsubject", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + token
          },
          body: JSON.stringify({ pattern: this.searchQuery })
        });
        if (!response.ok) {
          throw new Error("Failed to search subjects");
        }
        const data = await response.json();
        this.subjects = data.subjects;
      } catch (error) {
        console.error("Error searching subjects:", error);
      }
    },
    async deleteSubject(subjectId) {
      try {
        const response = await fetch(`http://localhost:5000/deletesubject/${subjectId}`, {
          method: "DELETE",
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to delete subject");
        }
        this.fetchSubjects();
      } catch (error) {
        console.error("Error deleting subject:", error);
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
  --danger:#d9534f;
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
  text-decoration:none;
}

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
  width:220px;
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
  padding:10px;
  display:flex;
  gap:8px;
  justify-content:center;
  border-top:1px solid #f1f4f6;
  border-bottom-left-radius:10px;
  border-bottom-right-radius:10px;
}

.btn-ghost{
  background:transparent;
  border:1px solid rgba(15,76,92,0.08);
  padding:8px 12px;
  border-radius:8px;
  color:var(--accent);
  cursor:pointer;
  font-weight:700;
}

.btn-danger{
  background:var(--danger);
  color:white;
  padding:8px 12px;
  border:none;
  border-radius:8px;
  cursor:pointer;
  font-weight:700;
}

.btn-ghost:hover{ background:rgba(15,76,92,0.04); }
.btn-danger:hover{ filter:brightness(0.95); }

.empty{ padding:36px; color:var(--muted); text-align:center; }

@media (max-width:980px){
  .sidebar{ display:none; }
  .main{ width:100%; padding:18px; }
  .list{ justify-content:center; }
}
</style>
