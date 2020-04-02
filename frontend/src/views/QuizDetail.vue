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
      <button
        type="button"
        class="start-btn btn btn-success"
        @click="enterQuiz"
      >
        Start Quiz
      </button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import TheNavbar from "@/components/base/TheNavbar.vue";

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
    ...mapActions("quiz", ["getQuizWithQuestions", "startQuizByUser"]),
    getQuizId() {
      return this.$route.params.id;
    },
    enterQuiz() {
      const quizId = this.getQuizId();
      this.startQuizByUser(quizId).then(() => {
        this.$router.push("/quiz/solve/");
      });
    }
  },
  created() {
    const quizId = this.$route.params.id;
    this.getQuizWithQuestions(quizId);
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
