<template>
  <div class="question">
    <p class="question-content mt-5">{{ question.question }}</p>
    <div
      class="answer"
      @click="checkElement(index)"
      v-for="(answer, index) in question.answers"
      :key="answer.id"
      v-bind:class="[
        answered ? (answer.is_correct ? 'good-answer' : 'bad-answer') : 'answer'
      ]"
    >
      <label
        ><input type="radio" name="answerRadio" class="mr-2" />{{
          answer.content
        }}</label
      >
    </div>
    <div class="explaination mt-3 mb-3" v-if="answered">
      <div id="accordion">
        <div class="card">
          <div class="card-header text-center">
            <h5>
              <a
                href="#collapse1"
                data-parent="#accordion"
                data-toggle="collapse"
                >Explaination</a
              >
            </h5>
          </div>
          <div id="collapse1" class="collapse">
            <div class="card-body">{{ question.explaination }}</div>
          </div>
        </div>
      </div>
    </div>
    <button
      class="question-btn btn btn-danger"
      v-if="!answered"
      @click="submitAnswer"
    >
      Answer
    </button>
    <button class="question-btn btn btn-danger" v-else>Next Question</button>
  </div>
</template>

<script>
export default {
  name: "Question",
  props: { question: Object },
  data() {
    return {
      answered: false
      // choice: null
    };
  },
  methods: {
    checkElement(index) {
      document.getElementsByClassName("answer")[
        index
      ].children[0].children[0].checked = true;
    },
    submitAnswer() {
      // sprawdź, który checkbox jest zaznaczony
      // wyślij rodzicowi $emit id odpowiedzi
      this.answered = true;
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
