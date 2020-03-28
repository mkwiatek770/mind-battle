<template>
  <div id="main">
    <div v-for="quiz in quizzes" :key="quiz.id">
      <Quiz :quiz="quiz" />
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import Quiz from "./Quiz.vue";

export default {
  name: "TheMain",
  components: {
    Quiz
  },
  data() {
    return {};
  },
  computed: mapState({
    quizzes: state => state.quiz.quizzes
  }),
  methods: mapActions("quizzes", ["getQuizzes"]),
  created() {
    this.$store.dispatch("quiz/getQuizzes");
  }
};
</script>

<style scoped>
#main {
  padding-top: 20px;
  height: 100%;
  width: 100%;
}
</style>
