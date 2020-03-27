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
          creator: "user1",
          image:
            "https://image.winudf.com/v2/image1/Y29tLmNhbmR5LnNvd2FyX0dpcmx5X3NjcmVlbl8wXzE1NTE2NDI5OTVfMDY3/screen-0.jpg?fakeurl=1&type=.jpg"
        },
        {
          id: 2,
          name: "Quiz duoa",
          category: {
            id: 1,
            name: "Nowa kategoria"
          },
          creator: "user2",
          image:
            "https://cdn.acidcow.com/pics/20190619/1560962877_s5j28jll8g.jpg"
        },
        {
          id: 3,
          name: "What is this ...",
          category: {
            id: 1,
            name: "python"
          },
          creator: "user3",
          image:
            "https://media.funalive.com/article/images/pretty_girls_is_why_were_all_here_640_01.jpg"
        }
      ]
    };
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
