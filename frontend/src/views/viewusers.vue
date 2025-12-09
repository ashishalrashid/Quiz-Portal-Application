<template>
  <div class="page">
    <aside class="sidebar" aria-label="Admin navigation">
      <RouterLink to="/admindash" class="nav-item" title="Home">
        <i class="fas fa-home nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Home</span>
      </RouterLink>

      <RouterLink to="/admindash/subjects" class="nav-item" title="Subjects">
        <i class="fas fa-book nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Subjects</span>
      </RouterLink>

      <RouterLink to="/admindash/user" class="nav-item disabled" title="Users">
        <i class="fas fa-user nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Users</span>
      </RouterLink>

      <RouterLink to="/admindash/stats" class="nav-item" title="Stats">
        <i class="fas fa-chart-bar nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Stats</span>
      </RouterLink>

      <a href="#" @click.prevent="logout" class="nav-item logout" role="button" title="Log out">
        <i class="fas fa-sign-out-alt nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Log Out</span>
      </a>
    </aside>

    <main class="main" role="main">
      <header class="header">
        <div>
          <h1 class="title">Users</h1>
          <p class="subtitle">Manage platform users</p>
        </div>

        <div class="controls">
          <div class="search">
            <input
              v-model="searchQuery"
              @keyup.enter="searchUsers"
              type="search"
              class="search-field"
              placeholder="Search users by name or email..."
              aria-label="Search users"
            />
            <button @click="searchUsers" class="search-btn" aria-label="Search users">
              <i class="fas fa-search" aria-hidden="true"></i>
            </button>
          </div>
        </div>
      </header>

      <section class="card-wrap" aria-live="polite">
        <table class="user-table" role="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Full Name</th>
              <th>Qualification</th>
              <th>Date of Birth</th>
              <th class="col-actions">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="!users || users.length === 0">
              <td colspan="7" class="empty">No users found.</td>
            </tr>

            <tr v-for="user in users" :key="user.id">
              <td class="cell-id">{{ user.id }}</td>
              <td class="cell-username">{{ user.username }}</td>
              <td class="cell-email">{{ user.email }}</td>
              <td class="cell-name">{{ user.full_name || "—" }}</td>
              <td class="cell-qual">{{ user.qualification || "—" }}</td>
              <td class="cell-dob">{{ user.dob || "—" }}</td>
              <td class="action-buttons">
                <button @click="deleteUser(user.id)" class="btn-danger" aria-label="Delete user">
                  Delete
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
import axios from "axios";
export default {
  name: "Users",
  data() {
    return {
      users: [],
      searchQuery: ""
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:5000/getusers", {
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`
          }
        });
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    async deleteUser(userId) {
      try {
        const token = localStorage.getItem("token");
        await axios.delete(`http://localhost:5000/deleteuser/${userId}`, {
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`
          }
        });
        this.fetchUsers();
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    },
    async searchUsers() {
      try {
        const response = await fetch("http://localhost:5000/getsearchuser", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          },
          body: JSON.stringify({ pattern: this.searchQuery })
        });

        if (!response.ok) {
          throw new Error("Failed to search users");
        }

        const data = await response.json();
        this.users = data.users;
      } catch (error) {
        console.error("Error searching users:", error);
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
:root {
  --sidebar-bg: #1f2933;
  --accent: #0f4c5c;
  --muted: #6b7280;
  --card-bg: #ffffff;
  --danger: #dc2626;
  --radius: 12px;
  --max-width: 1200px;
}

* { box-sizing: border-box; }

.page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(180deg, #f3f5f6, #e9ecef);
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.title { margin: 0; font-size: 1.4rem; font-weight: 700; }
.subtitle { margin: 4px 0 0; color: var(--muted); font-size: 0.95rem; }

.controls { display: flex; gap: 12px; align-items: center; }

.search { display: flex; gap: 8px; align-items: center; }

.search-field {
  border-radius: 10px;
  border: 1px solid #e6e9eb;
  padding: 8px 12px;
  min-width: 260px;
  outline: none;
}
.search-field:focus { box-shadow: 0 8px 20px rgba(15,76,92,0.06); border-color: var(--accent); }

.search-btn {
  border-radius: 10px;
  border: none;
  padding: 8px 12px;
  color: #fff;
  background: var(--accent);
  cursor: pointer;
}

.card-wrap {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 8px 24px rgba(11,23,40,0.04);
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
  font-size: 0.95rem;
}

.user-table thead th {
  text-align: left;
  padding: 12px 14px;
  background: #f7fafb;
  color: #0b1220;
  font-weight: 700;
  border-bottom: 1px solid #eef2f6;
}

.user-table tbody td {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
  color: #111827;
}

.user-table tbody tr:hover { background: #fcfdff; }

.action-buttons { display: flex; gap: 8px; align-items: center; }

.btn-danger {
  background: var(--danger);
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
}

.empty { text-align: center; padding: 22px; color: var(--muted); }

@media (max-width: 980px) {
  .sidebar { display: none; }
  .main { width: 100%; padding: 18px; }
  .user-table thead { display: none; }
  .user-table, .user-table tbody, .user-table tr, .user-table td { display: block; width: 100%; }
  .user-table tr { margin-bottom: 14px; border-radius: 8px; box-shadow: 0 6px 18px rgba(11,23,40,0.04); background: #fff; padding: 12px; }
  .user-table td { padding: 8px 10px; border: none; }
  .user-table td::before { content: attr(data-label); display: block; font-weight: 700; color: var(--muted); margin-bottom: 6px; }
  .col-actions { text-align: right; }
}
</style>
