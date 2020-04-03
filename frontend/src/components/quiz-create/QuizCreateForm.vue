<template>
  <div id="create-form" class="mt-5">
    <form>
      <div class="form-group mb-3">
        <label for="quiz-name">Quiz name</label>
        <input
          type="text"
          class="form-control"
          id="quiz-name"
          placeholder=""
          v-model="name"
        />
      </div>

      <div class="form-group mb-3">
        <label for="quiz-category">Category:</label>
        <select class="form-control" id="quiz-category" v-model="category_name">
          <option v-for="category in categories" :key="category.id">{{
            category.name
          }}</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="quiz-image">Image</label>
        <input type="file" name="image" id="quiz-image" @change="uploadImage" />
      </div>

      <h2 class="font-weight-bold">Questions</h2>
      <div
        class="question-container"
        v-for="index in questionCounter"
        :key="index"
      >
        <p
          class="font-weight-bold mt-2"
          style="padding-top: 10px; font-size: 1.2em;"
        >
          {{ index }}
        </p>
        <Question ref="questions" :idx="index" />
      </div>
      <button
        type="button"
        class="btn btn-success mt-3"
        @click="questionCounter++"
      >
        Add question
      </button>

      <div class="mt-5">
        <input type="checkbox" id="checkbox" v-model="publish" />
        <span for="checkbox" class="font-weight-bold">
          Publish
        </span>
      </div>

      <button
        type="button"
        class="btn btn-success create-btn mt-2"
        @click="createClick"
      >
        Create Quiz
      </button>
    </form>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import Question from "./Question.vue";

export default {
  name: "QuizCreateForm",
  components: {
    Question
  },
  data() {
    return {
      questionCounter: 0,
      name: "",
      image: null,
      category_name: "",
      publish: false,
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
  },
  methods: {
    ...mapActions("quiz", ["createQuiz"]),
    createClick() {
      var quizObj = {
        name: this.name,
        category_name: this.category_name,
        publish: this.publish
      };
      let questions = [];
      if (this.anyQuestion()) {
        for (var i = 0; i < this.$refs.questions.length; i++) {
          questions.push(this.$refs.questions[i].question);
        }
      }
      this.createQuiz({
        quiz: quizObj,
        questions: questions,
        image: this.image
      });
    },
    anyQuestion() {
      return Object.prototype.hasOwnProperty.call(this.$refs, "questions");
    },
    uploadImage(e) {
      this.image = e.target.files[0];
    }
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
