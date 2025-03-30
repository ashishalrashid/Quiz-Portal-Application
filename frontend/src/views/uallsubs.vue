<template>
    <div class="container">
        <div class="user-dashboard">
      <RouterLink to="/userdash" class="icon">
        <i class="fas fa-home"> Home</i>
      </RouterLink>
      <RouterLink to="/uallsubjects" class="disabled">
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
      <div class="top">
            <h2>All Subjects</h2>
            <input type="text" v-model="searchQuery" placeholder="Search..." class="field"/>
    
    <button @click="searchOtherSubjects" class="search-btn">
        <i class="fas fa-search"></i> Search
    </button>
          </div>
    <ul class="subs">
      <li 
        v-for="subject in subjects" 
        :key="subject.id" 
        class="sub_item"
      >
        <div @click="goToSubject(subject.id)">
          <h3 class="gwak">{{ subject.name }}</h3>
          <p>{{ subject.description }}</p>
        </div>
        <div class="action-buttons">
          <button @click="SubscribeSubject(subject.id)" class="but">Subscribe</button>
        </div>
      </li>
    </ul>
  </div>

    </div>

</template>


<script>
export default {
  name: "Subjects",
  data() {
    return {
      subjects: []
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
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to fetch subjects");
        }
        const data = await response.json();
        this.subjects = data.subjects;
        alert
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
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ pattern: this.searchQuery })
        });

        if (!response.ok) {
            throw new Error("Failed to fetch subjects");
        }

        const data = await response.json();
        this.subjects = data.subjects; 
    } catch (error) {
        console.error("Error searching subjects:", error);
    }
},
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    async SubscribeSubject(subjectId) {
      try {
        const response = await fetch(`http://localhost:5000/createusersubject/${subjectId}`, {
          method: "POST",
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed to delete subject");
        }
        alert("Subscribed!")
        this.fetchSubjects();
      } catch (error) {
        console.error("Error deleting subject:", error);
      }
    }
  }
};
</script>



<style>
html, body, #app {
  margin: 0;
}

.container {
    font-family: 'Times New Roman', Times, serif;
  display: flex;
  background-color: rgb(213, 213, 213);
  height: 100vh;
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
    justify-content: flex-start !important;
    margin-left: 10%;
    overflow-y: auto;
}
.subs {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    list-style: none;
    height: 100%;
    margin-top: 0px !important;
    width: 90% !important;
}
.sub_item {
  border: 1px solid #040404;
  border-radius: 25px;
  padding: 15px;
  cursor: pointer;
  margin: 20px !important;
  width: 150px;
  height: 250px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  font-size: larger;
  align-items: center;
}
.sub_item:hover {
  background-color: #ffffff;
  transform: scale(1.05);
}
.action-buttons{
    margin-top: auto;
    display: flex;
    justify-content: space-around;
}
.danger{
    background-color: red;
    margin: 10px;
    border: 1px;
    border-radius: 25px;
    
}
.but{
    background-color: #ffffff;
    margin: 10px;
    border: 1px;
    border-radius: 25px;
}
.all-subjects{
  margin-top:auto !important;
}
.gwak{
  font-size: 30px !important;
}
</style>