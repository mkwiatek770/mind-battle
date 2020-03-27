<template>
  <div id="create-form" class="mt-5">
    <form>
      <div class="form-group mb-3">
        <label for="quiz-name">Quiz name</label>
        <input type="text" class="form-control" id="quiz-name" placeholder="" />
      </div>

      <div class="form-group mb-3">
        <label for="quiz-category">Category:</label>
        <select class="form-control" id="quiz-category">
          <option v-for="category in categories" :key="category.id">{{
            category.name
          }}</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="quiz-image">Image</label>
        <input type="file" name="image" id="quiz-image" />
      </div>

      <h2 class="font-weight-bold">Questions</h2>
      <div
        class="question-container"
        v-for="index in questionCounter"
        :key="index"
      >
        <p
          class="font-weight-bold mt-2"
          style="border-top: 1px solid black; padding-top: 10px; font-size: 1.2em;"
        >
          {{ index }}
        </p>
        <Question />
      </div>
      <button
        type="button"
        class="btn btn-success mt-3"
        @click="questionCounter++"
      >
        Add question
      </button>

      <!-- Question components here -->
      <button type="button" class="btn btn-success create-btn mt-5">
        Create Quiz
      </button>
    </form>
  </div>
</template>

<script>
import Question from "./Question.vue";

export default {
  name: "QuizCreateForm",
  components: {
    Question
  },
  data() {
    return {
      questionCounter: 0,
      categories: [
        {
          id: 1,
          name: "python"
        },
        {
          id: 2,
          name: "javascript"
        }
      ]
    };
  }
};
</script>

<style scoped>
label {
  font-size: 1.3em;
  font-weight: bold;
  display: block;
}

.create-btn {
  display: block;
  width: 100%;
}
</style>
