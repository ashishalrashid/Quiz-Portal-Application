<template>
    <div class="container">
        <div class="admin-dashboard">
            <RouterLink to="/admindash" class="icon">
                <i class="fas fa-home"> Home</i>
            </RouterLink>
            <RouterLink to="/admindash/subjects" class="icon">
                <i class="fas fa-book circular-icon"> Subjects</i>
            </RouterLink>
            <RouterLink to="/admindash/user" class="icon">
                <i class="fas fa-user circular-icon"> Users</i>
            </RouterLink>
            <RouterLink to="/admindash/stats" class="icon">
                <i class="fas fa-chart-bar"> Stats</i>
            </RouterLink>
            <a href="#" @click.prevent="logout" class="icon">
                <i class="fas fa-sign-out-alt"> Log Out</i>
            </a>
        </div>
        
        <div class="subcontainer">
            <div class="top">
            <h2>Chapters</h2>
            <RouterLink :to="`/admindash/createchapter/${subjectId}`" 
                class="all-subjects"
            >
                <i class="fas fa-plus-circle"> Add Chapter</i>
            </RouterLink>

        </div>
            <ul class="subs">
                <li v-for="chapter in chapters" :key="chapter.id" class="sub_item">
                    <div>
                        <h3 class="gwak">{{ chapter.name }}</h3>
                        <p>{{ chapter.description }}</p>
                    </div>
                    <div class="action-buttons">
                        <button @click="goToEditChapter(chapter.id)" class="but">Edit</button>
                        <button @click="deleteChapter(chapter.id)" class="danger">Delete</button>
                    </div>
                </li>
            </ul>
        </div>
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
        async deleteSubject(subjectId) {
      try {
        const response = await fetch(`http://localhost:5000/deletechapter/${ChapterId}`, {
          method: "DELETE",
          headers: {
            "Accept": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          }
        });
        if (!response.ok) {
          throw new Error("Failed");
        }
        this.fetchSubjects();
      } catch (error) {
        console.error("Error", error);
      }
    },
        logout() {
            localStorage.removeItem("token");
            this.$router.push("/login");
        },
        goToEditChapter(chapterId) {
            this.$router.push(`/admindash/chapter/${chapterId}/edit`);
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
        }
    }
};
</script>

<style>
html, body, #app {
  margin: 0;
  height: 100%;
  width: 100%;
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
    width: 100%;
}
.top {
    display: flex;
    align-items: center;
}
.subs {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    list-style: none;
    height: 100%;
    width: 100%;
}
.sub_item {
  border: 1px solid #040404;
  border-radius: 25px;
  padding: 15px;
  cursor: pointer;
  margin: 10px;
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
.gwak {
    font-size: 40px;
}
.action-buttons {
    margin-top: auto;
    display: flex;
    justify-content: space-around;
}
.danger {
    background-color: red;
    margin: 10px;
    border: 1px;
    border-radius: 25px;
}
.but {
    background-color: #ffffff;
    margin: 10px;
    border: 1px;
    border-radius: 25px;
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
  margin: 50px;
}

.all-subjects i {
  margin-left: 8px;
}
.all-subjects:hover {
  background-color: #000000;
  transform: scale(1.1);
}
</style>