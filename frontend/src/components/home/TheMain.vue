<template>
  <div id="main">
    <div v-for="quiz in quizzes" :key="quiz.id">
      <Quiz :quiz="quiz" />
    </div>
  </div>
</template>

<script>
import Quiz from "./Quiz.vue";

export default {
  name: "TheMain",
  components: {
    Quiz
  },
  data() {
    return {
      quizzes: [
        {
          id: 1,
          name: "Quiz 1",
          category: {
            id: 1,
            name: "Nowa kategoria"
          },
          creator: "user1"
        },
        {
          id: 2,
          name: "Quiz duoa",
          category: {
            id: 1,
            name: "Nowa kategoria"
          },
          creator: "user2"
        },
        {
          id: 3,
          name: "What is this ...",
          category: {
            id: 1,
            name: "python"
          },
          creator: "user3"
        }
      ]
    };
  }
};
</script>

<style scoped>
#main {
  padding-top: 20px;
  background-color: green;
  height: 100%;
  width: 100%;
}
</style>
