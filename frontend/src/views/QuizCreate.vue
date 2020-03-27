<template>
  <div id="quiz-create" class="row">
    <div
      class="col-sm-9 col-md-8 col-lg-6 col-xl-5 mx-auto mt-5 p-5"
      style="background-color: white"
    >
      <h1 style="font-weight: bold; text-align: center;">Create new quiz</h1>
      <QuizCreateForm />
    </div>
  </div>
</template>

<script>
import QuizCreateForm from "@/components/quiz-create/QuizCreateForm.vue";

export default {
  name: "QuizCreate",
  components: {
    QuizCreateForm
  }
};
</script>
