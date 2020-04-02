<template>
  <div id="quiz-summary">
    <TheNavbar />
    <SummaryMain />
  </div>
</template>

<script>
import TheNavbar from "@/components/base/TheNavbar.vue";
import SummaryMain from "@/components/quiz-summary/SummaryMain.vue";

export default {
  name: "QuizSummary.vue",
  components: {
    TheNavbar,
    SummaryMain
  }
};
</script>
