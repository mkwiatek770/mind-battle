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
        <Question :question="recentQuiz.questions[currentQuestionIndex]" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import TheNavbar from "@/components/quiz-detail/TheNavbar.vue";
import TheHeader from "@/components/quiz-detail/TheHeader.vue";
import ProgressBar from "@/components/quiz-detail/ProgressBar.vue";
import Question from "@/components/quiz-detail/Question.vue";

export default {
  name: "QuizDetail",
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
    ...mapState("quiz", ["recentQuiz"])
  },
  methods: {
    ...mapActions("quiz", ["getQuizWithQuestions"])
  },
  created() {
    const quizId = this.$route.params.id;
    this.getQuizWithQuestions(quizId);
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
