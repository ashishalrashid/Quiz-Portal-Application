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
                <h2>Quizzes</h2>
                <button @click="goToCreateQuiz" class="all-subjects">
                    <i class="fas fa-plus-circle"> Add Quiz</i>
                </button>
                <input type="text" v-model="searchQuery" placeholder="Search..." class="field"/>
                <button @click="searchQuizzes" class="search-btn">
                    <i class="fas fa-search"></i>
                </button>
            </div>
            <table class="quiz-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Chapter ID</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Duration</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="quiz in quizzes" :key="quiz.id">
                        <td>{{ quiz.id }}</td>
                        <td>{{ quiz.name }}</td>
                        <td>{{ quiz.chapter_id }}</td>
                        <td>{{ quiz.start_date }}</td>
                        <td>{{ quiz.end_date }}</td>
                        <td>{{ quiz.time_duration }} minutes</td>
                        <td class="action-buttons">
                            <button @click="goToEditQuiz(quiz.id)" class="but">Edit</button>
                            <button @click="deleteQuiz(quiz.id)" class="danger">Delete</button>
                            <button @click="goToQuiz(quiz.id)" class="but">Go To Quiz</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: "Quizzes",
    data() {
        return {
            quizzes: [],
            searchQuery: ""
        };
    },
    created() {
        this.fetchQuizzes();
    },
    methods: {
        async fetchQuizzes() {
            try {
                const chapterId = this.$route.params.chapter_id;
                const response = await fetch(`http://localhost:5000/getquiz/${chapterId}`, {
                    headers: {
                        "Accept": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                });
                if (!response.ok) {
                    throw new Error("Failed to fetch quizzes");
                }
                const data = await response.json();
                this.quizzes = data.quizzes;
            } catch (error) {
                console.error("Error fetching quizzes:", error);
            }
        },
        async searchQuizzes() {
            try {
                const chapterId = this.$route.params.chapter_id; 
                const response = await fetch(`http://localhost:5000/getsearchquiz/${chapterId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    },
                    body: JSON.stringify({ pattern: this.searchQuery })
                });
                if (!response.ok) {
                    throw new Error("Failed to search quizzes");
                }
                const data = await response.json();
                this.quizzes = data.quizzes;
            } catch (error) {
                console.error("Error searching quizzes:", error);
            }
        },
        logout() {
            localStorage.removeItem("token");
            this.$router.push("/login");
        },
        goToEditQuiz(quizId) {
            this.$router.push(`/editquiz/${quizId}`);
        },
        goToCreateQuiz() {
            const chapterId = this.$route.params.chapter_id;
            this.$router.push(`/createquiz/${chapterId}`);
        },
        goToQuiz(quizID) {
            this.$router.push(`/quiz/${quizID}`);
        },
        async deleteQuiz(quizId) {
            try {
                const response = await fetch(`http://localhost:5000/deletequiz/${quizId}`, {
                    method: "DELETE",
                    headers: {
                        "Accept": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                });
                if (!response.ok) {
                    throw new Error("Failed to delete quiz");
                }
                this.fetchQuizzes();
            } catch (error) {
                console.error("Error deleting quiz:", error);
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
}

.quiz-table {
    width: 90%;
    border-collapse: collapse;
    margin-top: 20px;
}

.quiz-table th, .quiz-table td {
    border: 1px solid black;
    padding: 10px;
    text-align: left;
}

.quiz-table th {
    background-color: #f4f4f4;
}

.action-buttons {
    display: flex;
    gap: 10px;
}

.danger {
    background-color: red;
    border: none;
    color: white;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
}

.but {
    background-color: #ffffff;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
}

.all-quizzes {
    margin-top: auto !important;
}
</style>