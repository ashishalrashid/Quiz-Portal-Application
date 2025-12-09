<template>
  <div class="page">
    <aside class="sidebar" aria-label="Admin navigation">
      <router-link to="/admindash" class="nav-item">
        <i class="fas fa-home nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Home</span>
      </router-link>

      <router-link to="/admindash/subjects" class="nav-item">
        <i class="fas fa-book nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Subjects</span>
      </router-link>

      <router-link to="/admindash/user" class="nav-item">
        <i class="fas fa-user nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Users</span>
      </router-link>

      <router-link to="/admindash/stats" class="nav-item">
        <i class="fas fa-chart-bar nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Stats</span>
      </router-link>

      <a href="#" @click.prevent="logout" class="nav-item logout" role="button">
        <i class="fas fa-sign-out-alt nav-icon" aria-hidden="true"></i>
        <span class="nav-label">Log Out</span>
      </a>
    </aside>

    <main class="main">
      <header class="main-header">
        <h1 class="title">Chapters</h1>
        <button class="btn-primary" @click="goToCreateChapter">
          <i class="fas fa-plus-circle" aria-hidden="true"></i>
          <span>Add Chapter</span>
        </button>
      </header>

      <section class="cards">
        <ul class="list" aria-live="polite">
          <li
            v-for="chapter in chapters"
            :key="chapter.id"
            class="card"
            role="group"
          >
            <div
              class="card-body"
              @click="goToChapter(chapter.id)"
              role="button"
              tabindex="0"
              @keyup.enter="goToChapter(chapter.id)"
              :aria-label="`Open chapter ${chapter.name}`"
            >
              <h3 class="card-title">{{ chapter.name }}</h3>
              <p class="card-desc">{{ chapter.description || 'No description' }}</p>
            </div>

            <div class="card-actions">
              <button class="btn-ghost" @click.stop="goToEditChapter(chapter.id)">Edit</button>
              <button class="btn-danger" @click.stop="deleteChapter(chapter.id)">Delete</button>
            </div>
          </li>
        </ul>

        <div v-if="!chapters || chapters.length === 0" class="empty">
          No chapters available.
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "Chapters",
  data() {
    return {
      chapters: []
    };
  },
  created() {
    this.fetchChapters();
  },
  methods: {
    async fetchChapters() {
      try {
        const subjectId = this.$route.params.subject_id;
        const response = await fetch(`http://localhost:5000/getchapter/${subjectId}`, {
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to fetch chapters");
        }
        const data = await response.json();
        this.chapters = data.chapters;
      } catch (error) {
        console.error("Error fetching chapters:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToEditChapter(chapterId) {
      this.$router.push(`/editchapter/${chapterId}`);
    },
    goToChapter(chapterId) {
      this.$router.push(`/chapter/${chapterId}`);
    },
    async deleteChapter(chapterId) {
      try {
        const response = await fetch(`http://localhost:5000/deletechapter/${chapterId}`, {
          method: "DELETE",
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to delete chapter");
        }
        this.fetchChapters();
      } catch (error) {
        console.error("Error deleting chapter:", error);
      }
    },
    goToCreateChapter() {
      const subjectId = this.$route.params.subject_id;
      if (subjectId) {
        this.$router.push(`/createchapter/${subjectId}`);
      } else {
        console.error("Subject ID not found in URL params");
      }
    }
  }
};
</script>

<style scoped>
:root{
  --sidebar-bg: #1f2933;
  --accent: #0f4c5c;
  --card-bg: #ffffff;
  --muted: #6b7280;
  --danger: #d9534f;
  --radius: 12px;
  --gap: 16px;
  --max-width: 1100px;
}

*{box-sizing:border-box}

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
.nav-icon { width:28px; text-align:center; font-size:1.05rem; }
.logout { margin-top: auto; background: rgba(255,255,255,0.02); }

/* Main */
.main {
  flex: 1;
  padding: 28px;
  max-width: var(--max-width);
  margin: 0 auto;
  width: calc(100% - 260px);
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  gap: 12px;
}

.title { margin: 0; font-size: 1.4rem; }

.btn-primary {
  display: inline-flex;
  gap: 8px;
  align-items: center;
  background: linear-gradient(180deg,var(--accent), #083b45);
  color: #fff;
  border: none;
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
}

.cards { display: block; }

.list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.card {
  width: 220px;
  background: var(--card-bg);
  border-radius: 10px;
  border: 1px solid #e6e9eb;
  box-shadow: 0 8px 20px rgba(11,23,40,0.04);
  display: flex;
  flex-direction: column;
  min-height: 220px;
  transition: transform 120ms ease, box-shadow 120ms ease;
}

.card:hover { transform: translateY(-6px); box-shadow: 0 14px 36px rgba(11,23,40,0.08); }

.card-body {
  padding: 16px;
  cursor: pointer;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-title { font-size: 1.05rem; font-weight: 700; margin: 0; }
.card-desc { color: var(--muted); font-size: 0.92rem; margin: 0; min-height: 48px; }

.card-actions {
  padding: 10px;
  display: flex;
  gap: 8px;
  justify-content: center;
  border-top: 1px solid #f1f4f6;
  background: linear-gradient(180deg, rgba(0,0,0,0.02), rgba(0,0,0,0.01));
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.btn-ghost {
  background: transparent;
  border: 1px solid rgba(15,76,92,0.08);
  padding: 8px 12px;
  border-radius: 8px;
  color: var(--accent);
  cursor: pointer;
  font-weight: 700;
}

.btn-ghost:hover { background: rgba(15,76,92,0.04); }

.btn-danger {
  background: var(--danger);
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
}

.btn-danger:hover { filter: brightness(0.95); }

.empty {
  padding: 36px;
  color: var(--muted);
  text-align: center;
}

/* responsive */
@media (max-width: 980px) {
  .sidebar { display: none; }
  .main { width: 100%; padding: 18px; }
  .list { justify-content: center; }
}
</style>
