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
      <section class="card" aria-labelledby="edit-subject-heading">
        <h2 id="edit-subject-heading" class="heading">Edit Subject</h2>

        <form @submit.prevent="updateSubject" class="form" novalidate>
          <label for="Sub_name" class="label">Subject Name</label>
          <input
            id="Sub_name"
            v-model="Sub_name"
            type="text"
            class="input"
            placeholder="e.g. Linear Algebra"
            aria-required="false"
          />

          <label for="description" class="label">Description</label>
          <input
            id="description"
            v-model="description"
            type="text"
            class="input"
            placeholder="Short description"
            aria-required="false"
          />

          <div class="actions">
            <button type="submit" class="btn-primary">Update</button>
            <router-link to="/admindash/subjects" class="btn-secondary">Cancel</router-link>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "EditSubject",
  data() {
    return {
      Sub_name: "",
      description: ""
    };
  },
  created() {
    this.fetchSubject();
  },
  methods: {
    async fetchSubject() {
      try {
        const subjectId = this.$route.params.subject_id;
        const token = localStorage.getItem("token");
        const response = await axios.get(
          `http://localhost:5000/getsubject/${subjectId}`,
          {
            headers: {
              "Accept": "application/json",
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.Sub_name = response.data.subject.name;
        this.description = response.data.subject.description;
      } catch (error) {
        console.error("Error fetching subject:", error);
      }
    },
    async updateSubject() {
      try {
        const subjectId = this.$route.params.subject_id;
        const token = localStorage.getItem("token");
        const data = {
          name: this.Sub_name,
          description: this.description
        };
        const response = await axios.put(
          `http://localhost:5000/editsubject/${subjectId}`,
          data,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
            }
          }
        );
        console.log("Subject updated successfully:", response.data);
        this.$router.push("/admindash/subjects");
      } catch (error) {
        console.error("Error updating subject:", error);
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
  --sidebar-bg: #1f2933;
  --accent: #0f4c5c;
  --muted: #6b7280;
  --card-bg: #ffffff;
  --radius: 12px;
  --gap: 16px;
  --max-width: 920px;
}

*{box-sizing:border-box}

.page{
  display:flex;
  min-height:100vh;
  background: linear-gradient(180deg,#f3f5f6,#e9ecef);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
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
  transition:background 120ms ease, transform 120ms ease;
}

.nav-item:hover{ background: rgba(255,255,255,0.04); transform: translateY(-2px); }
.nav-icon{ width:28px; text-align:center; font-size:1.05rem; }
.logout{ margin-top:auto; background: rgba(255,255,255,0.02); }

.main{
  flex:1;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  padding:28px;
  width:calc(100% - 240px);
}

.card{
  width:100%;
  max-width:var(--max-width);
  background:var(--card-bg);
  border-radius:var(--radius);
  padding:28px;
  box-shadow:0 8px 24px rgba(16,24,40,0.06);
  margin-top:72px;
}

.heading{
  margin:0 0 14px 0;
  font-size:1.4rem;
  color:#0b1220;
}

.form{
  display:flex;
  flex-direction:column;
  gap:12px;
}

.label{
  font-size:0.9rem;
  color:var(--muted);
  font-weight:600;
}

.input{
  height:44px;
  padding:0 12px;
  border-radius:10px;
  border:1px solid #d1d5db;
  background:#fbfdff;
  font-size:1rem;
  color:#0b1220;
  transition: box-shadow 120ms ease, border-color 120ms ease, transform 120ms ease;
  outline:none;
}

.input::placeholder{ color:#9ca3af; }
.input:focus{
  border-color:var(--accent);
  box-shadow:0 8px 20px rgba(15,76,92,0.06);
  transform: translateY(-1px);
}

.actions{
  display:flex;
  gap:12px;
  margin-top:6px;
  align-items:center;
}

.btn-primary{
  background: linear-gradient(180deg,var(--accent), #083b45);
  color:#fff;
  border:none;
  padding:10px 18px;
  border-radius:10px;
  font-weight:700;
  cursor:pointer;
}

.btn-secondary{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding:10px 14px;
  border-radius:10px;
  text-decoration:none;
  color:#0b1220;
  background:#f3f4f6;
  border:1px solid #e6e9eb;
  font-weight:600;
}

@media (max-width: 880px){
  .sidebar{ display:none; }
  .main{ width:100%; padding:18px; }
  .card{ margin-top:20px; padding:18px; }
}
</style>
