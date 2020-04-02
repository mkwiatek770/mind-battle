<template>
  <div>
    <h1>Summary</h1>
    <h5>Your score: 72%</h5>
    <p>You completed "Quiz name" with 8 correct answers out of 11 questions</p>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("user", ["quiz"])
  }
};
</script>
