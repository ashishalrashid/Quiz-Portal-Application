<template>
  <div class="container">
    <div class="user-dashboard">
      <RouterLink to="/userdash" class="disabled">
        <i class="fas fa-home"> Home</i>
      </RouterLink>
      <RouterLink to="/uallsubjects" class="icon">
        <i class="fas fa-book circular-icon"> All Subjects</i>
      </RouterLink>
      <RouterLink to="/yourperformance" class="icon">
        <i class="fas fa-chart-bar"> Your  Performance</i>
      </RouterLink>
      <a href="#" @click.prevent="logout" class="icon">
        <i class="fas fa-sign-out-alt"> Log Out</i>
      </a>
    </div>
    <div class="subcontainer">
      <ul class="subs">
        <li 
          v-for="subject in subjects" 
          :key="subject.id" 
          class="sub_item"
          @click="goToSubject(subject.id)"
        >
          <h3 class="gwak">{{ subject.name }}</h3>
          <p>{{ subject.description }}</p>
        </li>
      </ul>
    </div>
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

<style>
html, body, #app {
  margin: 0;
  width: 100%;
}

.container {
  font-family: 'Times New Roman', Times, serif;
  display: flex;
  background-color: rgb(213, 213, 213);
  width: 100%;
}

.user-dashboard {
  display: flex;
  background-color: rgb(56, 56, 56);
  flex-direction: column;
  justify-content: center;
  padding: 10px;
  align-items: flex-start;
  width: 400px !important;
}

.icon {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 10px;
  border-radius: 250px;
  margin: 10px;
  color: rgb(255, 255, 255);
  width: 80%;
  font-family: 'Times New Roman', Times, serif;
}

.icon:hover {
  background-color: #000000;
  transform: scale(1.1);
}

.disabled {
  background-color: rgb(117, 116, 116);
  padding: 10px;
  border-radius: 250px;
  margin: 10px;
  width: 80%;
  color: aliceblue;
}

.subcontainer {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin-left: 10%;
  overflow-y: auto;
  width: 80%;
}

.subs {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  padding: 0;
}

.sub_item {
  border: 1px solid #040404;
  border-radius: 25px;
  padding: 15px;
  cursor: pointer;
  margin: 10px;
  width: 40%;
  transition: transform 0.3s;
}

.sub_item:hover {
  background-color: #ffffff;
  transform: scale(1.05);
}

.gwak {
  font-size: 24px;
  margin: 0 0 10px;
}

.sub_item p {
  margin: 0;
  font-size: 16px;
  color: #333;
}
</style>
