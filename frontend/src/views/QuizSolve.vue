<template>
  <div id="quiz-detail">
    <TheNavbar />
    <div class="row">
      <div
        id="question-element"
        class="col-sm-9 col-md-8 col-lg-6 col-xl-5 mx-auto mt-5 p-5"
        style="background-color: white"
      >
        <TheHeader :name="recentQuiz.name" />
        <ProgressBar
          :questionsDone="questionsDone"
          :totalQuestions="recentQuiz.questions.length"
        />
        <Question
          :question="recentQuiz.questions[currentQuestionIndex]"
          :lastQuestion="lastQuestion"
          @answered="userAnswer"
          @nextQuestion="userNextQuestionOrFinish"
          @finishQuiz="finishQuiz"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

import TheNavbar from "@/components/base/TheNavbar.vue";
import TheHeader from "@/components/quiz-solve/TheHeader.vue";
import ProgressBar from "@/components/quiz-solve/ProgressBar.vue";
import Question from "@/components/quiz-solve/Question.vue";

export default {
  name: "QuizSolve",
  components: {
    TheNavbar,
    TheHeader,
    ProgressBar,
    Question
  },
  data() {
    return {
      questionsDone: 0,
      currentQuestionIndex: 0,
      correctAnswers: 0,
      userAnswers: []
    };
  },
  computed: {
    ...mapState("quiz", ["recentQuiz", "quiz"]),
    lastQuestion() {
      return this.currentQuestionIndex == this.recentQuiz.questions.length - 1;
    }
  },
  methods: {
    ...mapMutations("user", [
      "resetQuizPoints",
      "incrementCorrectAnswers",
      "incrementQuestionNumber"
    ]),
    ...mapActions("quiz", ["finishQuizByUser"]),
    userAnswer(answerId, correct) {
      this.userAnswers.push(answerId);
      this.questionsDone += 1;
      this.incrementQuestionNumber();
      if (correct) {
        this.correctAnswers += 1;
        this.incrementCorrectAnswers();
      }
    },
    userNextQuestionOrFinish() {
      if (this.currentQuestionIndex < this.recentQuiz.questions.length) {
        this.currentQuestionIndex += 1;
      } else {
        this.$router.push("/quiz/summary");
      }
    },
    finishQuiz() {
      this.finishQuizByUser(this.recentQuiz.id);
      this.$router.push("/quiz/summary");
    }
  },
  created() {
    this.resetQuizPoints();
  }
};
</script>

<style scoped>
#quiz-detail {
  width: 100%;
  height: 100vh;
}

#question-element {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
