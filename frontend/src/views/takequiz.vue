<template>
    <div class="quiz-container">
      <div class="timer">Time Remaining: {{ formattedTime }}</div>
      
      <div v-if="currentQuestion">
        <h2>{{ currentQuestion.question }}</h2>
        <form @submit.prevent="submitAnswer">
          <div v-for="(option, index) in currentQuestion.options" :key="index">
            <label>
              <input type="radio" :value="index + 1" v-model.number="selectedOption">
              {{ option }}
            </label>
          </div>
          <button type="submit">Submit Answer</button>
        </form>
      </div>
      
      <div v-else>
        <h2>Quiz Completed!</h2>
        <p>Your Score: {{ score }} / {{ questions.length }}</p>
      </div>
  
      <div v-if="alertMessage" class="alert" :class="{ correct: isCorrect, wrong: !isCorrect }">
        {{ alertMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "QuizComponent",
    data() {
      return {
        questions: [],
        currentIndex: 0,
        selectedOption: null,
        score: 0,
        timeRemaining: 0, 
        timer: null,
        alertMessage: "",
        isCorrect: false
      };
    },
    computed: {
      currentQuestion() {
        return this.questions[this.currentIndex];
      },
      formattedTime() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
      }
    },
    created() {
      this.fetchQuiz();
    },
    methods: {
      async fetchQuiz() {
        try {
          const token = localStorage.getItem("token");
          const quizId = this.$route.params.quiz_id;
          const response = await fetch(`http://localhost:5000/getquiz/${quizId}`, {
            headers: {
              "Accept": "application/json",
              "Authorization": "Bearer " + token
            }
          });
          if (!response.ok) {
            throw new Error("Failed to fetch quiz");
          }
          const data = await response.json();
          const quiz = data.quizzes[0];
          this.questions = quiz.questions || [];
          this.timeRemaining = (quiz.duration || 0) * 60;
          this.startTimer();
        } catch (error) {
          console.error("Error fetching quiz:", error);
        }
      },
      startTimer() {
        if (this.timer) clearInterval(this.timer);
        this.timer = setInterval(() => {
          if (this.timeRemaining > 0) {
            this.timeRemaining--;
          } else {
            clearInterval(this.timer);
            this.autoSubmit();
          }
        }, 1000);
      },
      submitAnswer() {
        if (!this.selectedOption) {
          alert("Please select an answer.");
          return;
        }
        if (this.selectedOption === this.currentQuestion.answer) {
          this.alertMessage = "Correct!";
          this.isCorrect = true;
          this.score++;
        } else {
          this.alertMessage = "Wrong!";
          this.isCorrect = false;
        }
        this.selectedOption = null;
        setTimeout(() => {
          this.alertMessage = "";
          this.currentIndex++;
          if (this.currentIndex >= this.questions.length) {
            clearInterval(this.timer);
            this.submitScore();
          }
        }, 1500);
      },
      autoSubmit() {
        alert("Time's up! Auto submitting the quiz.");
        this.submitScore();
      },
      async submitScore() {
        try {
          const quizId = this.$route.params.quiz_id;
          const token = localStorage.getItem("token");
          const response = await axios.post(
            `http://localhost:5000/submitscore/${quizId}`,
            { score: this.score },
            {
              headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
              }
            }
          );
          alert("Score submitted successfully!");
          this.$router.push("/yourperformance");
        } catch (error) {
          console.error("Error submitting score:", error);
          alert("Error submitting score.");
        }
      }
    },
    beforeUnmount() {
      if (this.timer) clearInterval(this.timer);
    }
  };
  </script>
  
  <style scoped>
  .quiz-container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    font-family: 'Times New Roman', Times, serif;
    background-color: #f9f9f9;
    border-radius: 10px;
    text-align: center;
  }
  .timer {
    font-size: 1.2em;
    margin-bottom: 20px;
    font-weight: bold;
  }
  form {
    text-align: left;
  }
  label {
    display: block;
    margin: 10px 0;
  }
  button {
    margin-top: 10px;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    background-color: #003f54;
    color: #fff;
    cursor: pointer;
  }
  button:hover {
    background-color: #000;
  }
  .alert {
    margin-top: 20px;
    padding: 10px;
    font-weight: bold;
  }
  .correct {
    color: green;
  }
  .wrong {
    color: red;
  }
  </style>
  