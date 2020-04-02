<template>
  <div id="quiz-create">
    <TheNavbar />
    <div class="row">
      <div
        class="col-sm-9 col-md-8 col-lg-6 col-xl-5 mx-auto mt-5 p-5"
        style="background-color: white"
      >
        <h1 style="font-weight: bold; text-align: center;">Create new quiz</h1>
        <QuizCreateForm />
      </div>
    </div>
  </div>
</template>

<script>
import TheNavbar from "@/components/base/TheNavbar.vue";
import QuizCreateForm from "@/components/quiz-create/QuizCreateForm.vue";

export default {
  name: "QuizCreate",
  components: {
    TheNavbar,
    QuizCreateForm
  }
};
</script>
