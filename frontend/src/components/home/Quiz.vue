<template>
  <div
    class="quiz"
    v-bind:style="{ 'background-image': 'url(' + quiz.image + ')' }"
    @click="redirectToDetail(quiz.id)"
  >
    <div class="row bottom-bar">
      <div class="col">
        <div class="row">
          <div class="col">
            <h1 class="quiz-title">{{ quiz.name }}</h1>
          </div>
        </div>
        <div class="row">
          <div class="col-6">
            <p>Created by: {{ quiz.creator }}</p>
          </div>
          <div class="col-6">
            <p>Category: {{ quiz.category.name }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Quiz",
  props: {
    quiz: Object
  },
  data() {
    return {};
  },
  methods: {
    redirectToDetail(id) {
      this.$router.push(`/quiz/${id}`);
    }
  }
};
</script>

<style scoped>
.quiz {
  width: 60%;
  margin: 0 auto 40px auto !important;
  background-size: cover;
  background-position: center;
  height: 400px;
  color: white;
  position: relative;
  opacity: 0.95;
}

@media only screen and (max-width: 1000px) {
  .quiz {
    width: 80%;
  }
}

.quiz:hover {
  opacity: 1;
  cursor: pointer;
}

.bottom-bar {
  background-color: rgb(200, 200, 200, 0.5);
  position: absolute;
  bottom: 0;
  width: 100%;
}

.quiz-title {
  text-align: left;
}
</style>
