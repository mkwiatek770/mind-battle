<template>
  <div id="main">
    <div v-for="quiz in quizzes" :key="quiz.id">
      <Quiz :quiz="quiz" />
    </div>
  </div>
</template>

<script>
import Quiz from "./Quiz.vue";
import axios from "axios";

export default {
  name: "TheMain",
  components: {
    Quiz
  },
  data() {
    return {
      quizzes: []
    };
  },
  mounted() {
    axios
      .get("http://localhost:8000/api/v1/quizzes")
      .then(response => (this.quizzes = response.data));
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
