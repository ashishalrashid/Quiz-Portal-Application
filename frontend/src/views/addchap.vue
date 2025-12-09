<template>
  <div class="page">
    <aside class="sidebar" aria-label="Admin dashboard navigation">
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

      <!-- kept click handler and href semantics but improved accessibility -->
      <a href="#" @click.prevent="logout" class="nav-item logout" role="button" title="Log out">
        <i class="fas fa-sign-out-alt nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Log Out</span>
      </a>
    </aside>

    <main class="main">
      <section class="form-card" aria-labelledby="create-chapter-heading">
        <h2 id="create-chapter-heading" class="heading">Create Chapter</h2>

        <form @submit.prevent="NewSub" class="form" novalidate>
          <div class="field">
            <label for="Sub_name" class="label">Chapter Name</label>
            <input
              id="Sub_name"
              v-model="Sub_name"
              type="text"
              class="input"
              required
              placeholder="Enter chapter name"
              aria-required="true"
            />
          </div>

          <div class="field">
            <label for="description" class="label">Description</label>
            <input
              id="description"
              v-model="description"
              type="text"
              class="input"
              required
              placeholder="Short description of the chapter"
              aria-required="true"
            />
          </div>

          <div class="actions">
            <button type="submit" class="btn-primary">Create</button>
            <router-link :to="`/admindash/subject/${$route.params.subject_id || ''}`" class="btn-secondary">
              Cancel
            </router-link>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      Sub_name: "",
      description: "",
    };
  },
  methods: {
    async NewSub() {
      if (!this.Sub_name || !this.description) {
        alert("All fields are required!");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        const subjectId = this.$route.params.subject_id;
        const response = await axios.post(
          `http://localhost:5000/createchapter/${subjectId}`,
          {
            name: this.Sub_name,
            description: this.description,
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        console.log("Subject created successfully:", response.data);
        this.$router.push(`/admindash/subject/${subjectId}`);
      } catch (error) {
        console.error("Error:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Layout & type */
:root{
  --sidebar-bg: #1f2933; /* dark slate */
  --accent: #0f4c5c; /* deep teal */
  --muted: #6b7280;
  --card-bg: #ffffff;
  --radius: 12px;
  --gap: 16px;
  --max-width: 900px;
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
  align-items: stretch;
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
  font-size: 0.98rem;
}
.nav-item .nav-icon {
  width: 28px;
  text-align: center;
  font-size: 1.05rem;
  opacity: 0.95;
}
.nav-item .nav-label {
  display: inline-block;
}
.nav-item:hover,
.nav-item:focus {
  background: rgba(255,255,255,0.04);
  transform: translateY(-2px);
  outline: none;
}
.logout {
  margin-top: auto;
  background: rgba(255,255,255,0.02);
}
.logout:hover {
  background: rgba(255,255,255,0.06);
}

/* Main area */
.main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: var(--container-padding);
  gap: var(--gap);
}

/* Card */
.form-card {
  width: 100%;
  max-width: var(--max-width);
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: 0 6px 18px rgba(16,24,40,0.06);
  margin-top: 72px;
}

/* Heading */
.heading {
  margin: 0 0 14px 0;
  font-size: 1.5rem;
  color: #0b1220;
}

/* Form */
.form {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label {
  font-size: 0.9rem;
  color: var(--muted);
  font-weight: 600;
}

/* Inputs */
.input {
  height: 44px;
  padding: 0 12px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  background: #fbfdff;
  font-size: 1rem;
  color: #0b1220;
  transition: box-shadow 120ms ease, border-color 120ms ease, transform 120ms ease;
  outline: none;
}
.input::placeholder {
  color: #9ca3af;
}
.input:focus {
  border-color: var(--accent);
  box-shadow: 0 4px 14px rgba(15,76,92,0.08);
  transform: translateY(-1px);
}

/* Actions */
.actions {
  display: flex;
  gap: 12px;
  margin-top: 6px;
  align-items: center;
}

.btn-primary {
  background: linear-gradient(180deg, var(--accent), #083b45);
  color: #fff;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease, opacity 120ms ease;
}
.btn-primary:hover,
.btn-primary:focus {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(15,76,92,0.18);
}
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #0b1220;
  background: #f3f4f6;
  border: 1px solid #e6e9eb;
  font-weight: 600;
}
.btn-secondary:hover {
  background: #eef2f6;
  transform: translateY(-2px);
}

/* Responsiveness */
@media (max-width: 880px) {
  .sidebar {
    width: 64px;
    padding: 14px 8px;
    gap: 6px;
  }
  .nav-item .nav-label { display: none; }
  .main { padding: 16px; }
  .form-card { margin-top: 20px; padding: 18px; }
}
</style>
