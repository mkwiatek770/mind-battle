<template>
  <div id="summary-main">
    <h1 class="mb-5">Summary</h1>
    <h5>Your score: {{ getPercentage() }}%</h5>
    <p>
      You completed "Quiz name" with {{ quiz.correctAnswers }} correct answers
      out of {{ quiz.questionNumber }} questions
    </p>
    <button class="btn btn-success mt-3">Go to home page</button>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("user", ["quiz"]),
    ...mapState("quiz", ["recentQuiz"])
  },
  methods: {
    getPercentage() {
      if (this.quiz.questionNumber == 0) {
        return 0;
      }
      return Math.floor(
        (this.quiz.correctAnswers / this.quiz.questionNumber) * 100
      );
    }
  }
};
</script>

<style scoped>
#summary-main {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%;
  background-color: white;
  padding: 30px 20px;
}
</style>
