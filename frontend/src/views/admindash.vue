<template>
    <div class="container">
    <div class="admin-dashboard">
              <RouterLink to="/admindash" class="disabled">
                <i class="fas fa-home"> Home</i>
              </RouterLink>
              <RouterLink to="/admindash/subjects" class="icon">
                <i class="fas fa-book circular-icon">  Subjects</i>
              </RouterLink>
              <RouterLink to="/admindash/user" class="icon">
                <i class="fas fa-user circular-icon">  Users</i>
                </RouterLink>
              <RouterLink to="/admindash/stats" class="icon">
                <i class="fas fa-chart-bar">  Stats</i>
              </RouterLink>
              <a href="#" @click.prevent="logout" class="icon">
                <i class="fas fa-sign-out-alt">  Log Out</i>
              </a>
    </div>
    <div class="subcontainer">
    <div class="subject-list">
    <h2>Subjects</h2>
    <ul class="subs">
      <li 
        v-for="subject in subjects.slice(0, 4)" 
        :key="subject.id" 
        class="sub_item"
        @click="goToSubject(subject.id)"
      >
        <h3>{{ subject.name }}</h3>
        <p>{{ subject.description }}</p>
      </li>
    </ul>
    <RouterLink to="/admindash/subjects" class="all-subjects">
  All Subjects <i class="fas fa-arrow-right"></i>
</RouterLink>

    </div>
    <div class="stats">
        <h2>Statistics</h2>
        <div class="stat">
  <ul class="count">
    <li class="sta">User Count: <span class="big-number">{{ counts.user_count }}</span></li>
    <li class="sta">Quiz Count: <span class="big-number">{{ counts.quiz_count }}</span></li>
    <li class="sta">Subject Count: <span class="big-number">{{ counts.subject_count }}</span></li>
    <li class="sta">Chapter Count: <span class="big-number">{{ counts.chapter_count }}</span></li>
  </ul>
</div>
    </div>
</div>
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


<style>
html, body, #app {
  margin: 0;
  width: 100%;
  height: 100% !important;
}

.container {
    font-family: 'Times New Roman', Times, serif;
  display: flex;
  background-color: rgb(213, 213, 213);
  width: 100%;
}

.admin-dashboard {
  display: flex;
  background-color: rgb(56, 56, 56);
  flex-direction: column;
  justify-content: center;
  padding: 10px;
  align-items: flex-start;
  width: 250px;
}
.icon {
    display: flexbox;
    justify-content: center;
    align-items: flex-start;
    padding: 10px;
    border-radius: 250px;
    margin:10px;
    color: rgb(255, 255, 255);
    width: 80%;
    font-family: 'Times New Roman', Times, serif;
}
.icon:hover {
  background-color: #000000;
  transform: scale(1.1);
}
.disabled{
    display: flex !important;
    justify-content: center !important;
    text-decoration: none !important;
    background-color: rgb(117, 116, 116);
    padding: 10px;
    border-radius: 250px;
    margin:10px;
    width: 80%;
    color:aliceblue;
}
.subcontainer {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    margin-left: 10%;
    width: 100%;
}
.subs {
    display: flex;
    justify-content: space-around;
    list-style: none;
    height: 300px !important;

}
.sub_item {
  border: 1px solid #040404;
  border-radius: 25px;
  padding: 15px;
  cursor: pointer;
  margin: 10px;
  width: 150px !important;
}
.sub_item:hover {
  background-color: #ffffff;
  transform: scale(1.05);
}

.all-subjects {
  text-decoration: none;
  color: #fff; 
  background-color: #003f54; 
  padding: 10px 15px;
  border: none;
  border-radius: 25px;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  font-size: 1em;
  margin-bottom: auto;
}

.all-subjects i {
  margin-left: 8px;
}
.count{
    display: flex;;
    justify-content: space-around;
    height: 100%;
}
.subject-list {
  margin: 0px;
}

.sta {
    list-style: none;
    border: 1px solid #040404;
    border-radius: 25px;
    padding: 10px;
    margin: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 30%;
    height: 100%;
}
.sta:hover {
    transform: scale(1.05);
}

.stat .big-number {
  font-size: 3em;
  font-weight: bold;
  color: #003f54;
  text-decoration: none;

}
</style>