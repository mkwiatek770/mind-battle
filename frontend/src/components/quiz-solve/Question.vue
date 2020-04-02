<template>
  <div class="question">
    <p class="question-content mt-5">{{ question.question }}</p>
    <div
      class="answer"
      @click="selectElement(index, answer.id)"
      v-for="(answer, index) in question.answers"
      :key="answer.id"
      v-bind:class="[
        answered ? (answer.is_correct ? 'good-answer' : '') : 'answer'
      ]"
    >
      <label
        ><input
          type="radio"
          name="answerRadio"
          class="mr-2"
          :disabled="answered"
        />{{ answer.content }}</label
      >
    </div>
    <div class="explanation mt-3 mb-3" v-if="answered">
      <div id="accordion">
        <div class="card">
          <div class="card-header text-center">
            <h5>
              <a
                href="#collapse1"
                data-parent="#accordion"
                data-toggle="collapse"
                >explanation</a
              >
            </h5>
          </div>
          <div id="collapse1" class="collapse">
            <div class="card-body">{{ question.explanation }}</div>
          </div>
        </div>
      </div>
    </div>
    <button
      class="question-btn btn btn-danger"
      v-if="!answered"
      @click="submitAnswer"
      :disabled="!choice"
    >
      Answer
    </button>
    <button
      class="question-btn btn btn-danger"
      v-else-if="lastQuestion"
      @click="finishQuiz"
      :disabled="!choice"
    >
      Finish quiz
    </button>
    <button class="question-btn btn btn-danger" v-else @click="nextQuestion">
      Next Question
    </button>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Question",
  props: { question: Object, lastQuestion: Boolean },
  data() {
    return {
      answered: false,
      choice: null,
      correct: null
    };
  },
  computed: {
    ...mapActions("quiz", ["finishQuizByUser"])
  },
  methods: {
    selectElement(index, answerId) {
      if (!this.answered) {
        document.getElementsByClassName("answer")[
          index
        ].children[0].children[0].checked = true;

        this.choice = parseInt(answerId);
        this.correct = this.question.answers[index].is_correct;
      }
    },
    submitAnswer() {
      this.answered = true;
      this.$emit("answered", this.choice, this.question.id, this.correct);
    },
    nextQuestion() {
      this.$emit("nextQuestion");
      this.answered = false;
      this.choice = null;
      this.correct = null;
    },
    finishQuiz() {
      this.$emit("finishQuiz");
    }
  }
};
</script>

<style scoped>
.question-content {
  font-weight: bold;
  font-size: 1.5em;
}

.answer {
  border: 1px solid rgb(204, 197, 197);
  /* border-radius: 10%; */
  padding: 10px 20px;
  margin: 10px 0 !important;
  transition: background-color 0.3s;
}

.good-answer {
  background-color: green;
}

.bad-answer {
  background-color: red;
}

.answer:hover {
  cursor: pointer;
  background-color: rgb(232, 235, 238);
}
.good-answer:hover {
  background-color: green;
}

.answer label {
  font-size: 1.2em;
}

.question-btn {
  width: 100%;
  font-size: 1.2em;
}

.card-body {
  font-size: 1.2em;
}
</style>
