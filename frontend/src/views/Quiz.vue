<template>
  <div class="quiz">
    <QuizList msg="List of quizzes" />
  </div>
</template>

<script>
// @ is an alias to /src
import QuizList from '@/components/QuizList.vue';

export default {
  name: 'Quiz',
  components: {
    QuizList,
  },
};
</script>
