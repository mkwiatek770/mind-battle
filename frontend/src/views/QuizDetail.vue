<template>
  <div id="quiz-detail">
    <TheNavbar />
    <div class="row quiz-info">
      <div class="col-12">
        <h1 class="text-center font-weight-bold">Sample name</h1>
        <p>Quiz description ....</p>
      </div>
      <img
        src="https://miro.medium.com/max/3000/1*MI686k5sDQrISBM6L8pf5A.jpeg"
        height="400"
        width="100%"
      />
      <router-link class="start-btn btn btn-success" to="/quiz/solve"
        >Start Quiz</router-link
      >
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import TheNavbar from "@/components/quiz-detail/TheNavbar.vue";

export default {
  name: "QuizDetail",
  components: {
    TheNavbar
  },
  data() {
    return {
      questionsDone: 0,
      currentQuestionIndex: 0,
      correctAnswers: 0,
      userAnswers: [],
      image: "https://miro.medium.com/max/3000/1*MI686k5sDQrISBM6L8pf5A.jpeg"
    };
  },
  props: {
    quizInfo: Object
  },
  computed: {
    ...mapState("quiz", ["recentQuiz"])
  },
  methods: {
    ...mapActions("quiz", ["getQuizWithQuestions"]),
    getQuizId() {
      return this.$route.params.id;
    }
  },
  created() {
    const quizId = this.$route.params.id;
    // if (this.quiz.id != quizId) {
    this.getQuizWithQuestions(quizId);
    // }
  }
};
</script>

<style scoped>
.quiz-info {
  position: absolute;
  background-color: white;
  width: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.start-btn {
  width: 100%;
}
</style>
