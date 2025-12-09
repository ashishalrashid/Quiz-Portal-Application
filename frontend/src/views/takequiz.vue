<template>
  <div class="quiz-page">
    <header class="quiz-header">
      <div class="meta">
        <div class="title">Quiz</div>
        <div class="progress">
          <div class="progress-text">Question {{ currentIndex + 1 }} / {{ questions.length || 1 }}</div>
          <div class="progress-bar" aria-hidden="true">
            <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="timer" role="timer" aria-live="polite">
        <svg viewBox="0 0 36 36" class="timer-ring" aria-hidden="true">
          <path class="ring-bg" d="M18 2a16 16 0 1 0 0 32 16 16 0 1 0 0-32" />
          <path
            class="ring-fg"
            :stroke-dasharray="timerDashArray"
            d="M18 2a16 16 0 1 0 0 32 16 16 0 1 0 0-32"
          />
        </svg>
        <div class="time-text" :aria-label="formattedTime">{{ formattedTime }}</div>
      </div>
    </header>

    <main class="quiz-main">
      <section v-if="currentQuestion" class="question-card" aria-labelledby="question-heading">
        <h2 id="question-heading" class="question-text">{{ currentQuestion.question }}</h2>

        <form @submit.prevent="submitAnswer" class="options" autocomplete="off">
          <fieldset class="options-field" :aria-describedby="'hint-' + currentIndex">
            <legend class="sr-only">Answer choices</legend>

            <label
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              class="option"
              :class="{ selected: selectedOption === index + 1 }"
            >
              <input
                type="radio"
                :value="index + 1"
                v-model.number="selectedOption"
                :name="'q' + currentIndex"
                class="option-input"
              />
              <span class="option-text">{{ option }}</span>
            </label>

            <div :id="'hint-' + currentIndex" class="hint">Select one option and submit.</div>
          </fieldset>

          <div class="controls">
            <button type="submit" class="btn-primary" :disabled="!selectedOption">Submit Answer</button>
            <button type="button" class="btn-muted" @click="skipQuestion" :disabled="!questions.length">Skip</button>
          </div>
        </form>
      </section>

      <section v-else class="result-card" aria-live="polite">
        <h2 class="result-title">Quiz Completed!</h2>
        <p class="result-score">Your Score: <strong>{{ score }}</strong> / {{ questions.length }}</p>
        <div class="result-actions">
          <button class="btn-primary" @click="submitScore">Submit Score</button>
          <router-link to="/yourperformance" class="btn-secondary">View Performance</router-link>
        </div>
      </section>

      <div v-if="alertMessage" class="toast" :class="{ ok: isCorrect, bad: !isCorrect }" role="status">
        {{ alertMessage }}
      </div>
    </main>
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
      return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    },
    progressPercent() {
      if (!this.questions.length) return 0;
      return Math.round(((this.currentIndex) / this.questions.length) * 100);
    },
    timerDashArray() {
      const total = 100;
      if (!this._durationSeconds || this._durationSeconds === 0) return `${total} ${total}`;
      const pct = Math.max(0, (this.timeRemaining / this._durationSeconds) * 100);
      return `${(pct / 100) * 100} ${total}`;
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
        const response = await fetch(`http://localhost:5000/usergetquiz/${quizId}`, {
          headers: {
            Accept: "application/json",
            Authorization: "Bearer " + token
          }
        });
        if (!response.ok) throw new Error("Failed to fetch quiz");
        const data = await response.json();
        if (data.questions && data.questions.length > 0) {
          this.questions = data.questions.map(q => ({
            question: q.question,
            options: [q.option1, q.option2, q.option3, q.option4],
            answer: q.answer
          }));
          this.timeRemaining = (data.duration || 0) * 60;
          this._durationSeconds = this.timeRemaining;
          this.startTimer();
        }
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
      }, 900);
    },
    skipQuestion() {
      this.selectedOption = null;
      this.currentIndex++;
      if (this.currentIndex >= this.questions.length) {
        clearInterval(this.timer);
        this.submitScore();
      }
    },
    autoSubmit() {
      alert("Time's up! Auto submitting the quiz.");
      this.submitScore();
    },
    async submitScore() {
      try {
        const quizId = this.$route.params.quiz_id;
        const token = localStorage.getItem("token");
        await axios.post(
          `http://localhost:5000/submitscore/${quizId}`,
          { score: this.score },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
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
:root {
  --card-bg: #ffffff;
  --accent: #0f4c5c;
  --muted: #6b7280;
  --good: #16a34a;
  --bad: #dc2626;
  --radius: 12px;
}

* { box-sizing: border-box; }

.quiz-page {
  max-width: 820px;
  margin: 36px auto;
  padding: 18px;
  font-family: Inter, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  margin-bottom: 18px;
}

.meta { flex: 1; }

.title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.progress {
  width: 100%;
}

.progress-text {
  font-size: 0.85rem;
  color: var(--muted);
  margin-bottom: 6px;
}

.progress-bar {
  height: 8px;
  background: #eef2f5;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), #083b45);
  width: 0%;
  transition: width 300ms ease;
}

.timer {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 120px;
}

.timer-ring { width: 48px; height: 48px; transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: #eef2f5; stroke-width: 3.6; stroke-linecap: round; }
.ring-fg { fill: none; stroke: #0f4c5c; stroke-width: 3.6; stroke-linecap: round; transition: stroke-dasharray 500ms linear; }

.time-text {
  font-weight: 700;
  color: #0b1220;
  min-width: 48px;
  text-align: left;
}

.quiz-main { background: var(--card-bg); padding: 22px; border-radius: var(--radius); box-shadow: 0 8px 30px rgba(11,23,40,0.06); }

.question-card { margin-bottom: 8px; }

.question-text {
  font-size: 1.15rem;
  margin: 0 0 14px 0;
}

.options-field { border: none; padding: 0; margin: 0; }

.option {
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid #eef2f5;
  padding: 10px 12px;
  border-radius: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease;
  user-select: none;
}

.option.selected {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(11,23,40,0.06);
  border-color: rgba(15,76,92,0.14);
  background: linear-gradient(180deg, rgba(15,76,92,0.03), rgba(15,76,92,0.02));
}

.option-input {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
}

.option-text { font-size: 0.98rem; color: #0b1220; }

.hint { font-size: 0.82rem; color: var(--muted); margin-top: 6px; }

.controls { display: flex; gap: 12px; margin-top: 8px; justify-content: flex-end; }

.btn-primary {
  background: linear-gradient(180deg, var(--accent), #083b45);
  color: #fff;
  border: none;
  padding: 10px 14px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; transform: none; box-shadow: none; }

.btn-muted {
  background: transparent;
  border: 1px solid #e6e9eb;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.result-card { text-align: center; padding: 22px; }

.result-title { font-size: 1.3rem; margin-bottom: 8px; }
.result-score { font-size: 1.05rem; color: #0b1220; }

.result-actions { margin-top: 16px; display: flex; gap: 12px; justify-content: center; }

.btn-secondary {
  display: inline-flex;
  align-items: center;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #0b1220;
  background: #f3f4f6;
  border: 1px solid #e6e9eb;
  font-weight: 600;
}

.toast {
  position: fixed;
  right: 20px;
  bottom: 24px;
  padding: 12px 14px;
  border-radius: 10px;
  color: white;
  font-weight: 700;
  box-shadow: 0 8px 24px rgba(11,23,40,0.12);
}
.toast.ok { background: var(--good); }
.toast.bad { background: var(--bad); }

.sr-only { position: absolute !important; height: 1px; width: 1px; overflow: hidden; clip: rect(1px,1px,1px,1px); white-space: nowrap; }

@media (max-width: 720px) {
  .quiz-page { padding: 12px; margin: 18px auto; }
  .quiz-header { flex-direction: column; align-items: flex-start; gap: 12px; }
  .timer { min-width: auto; }
  .controls { justify-content: stretch; flex-direction: column; }
  .btn-primary, .btn-muted { width: 100%; }
}
</style>
