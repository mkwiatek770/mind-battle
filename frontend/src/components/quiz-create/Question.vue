<template>
  <div
    class="question mt-3"
    style="border-bottom: 1px solid black; padding-bottom: 10px;"
  >
    <div class="form-group mb-3">
      <label for="quiz-name">Question</label>
      <input type="text" class="form-control" id="quiz-name" placeholder="" />
    </div>

    <div class="form-group mb-3">
      <label for="quiz-name">Explaination</label>
      <input type="text" class="form-control" id="quiz-name" placeholder="" />
    </div>

    <div class="row">
      <div class="col-2 align-middle" style="padding: 0; height: 48px;">
        <h5 style="line-height: 48px;">Answers</h5>
      </div>
      <div class="col-lg-4 col-md-5 ml-auto text-right">
        <button
          type="button"
          class="answer-action-btn add-btn"
          @click="addAnswer"
        >
          <font-awesome-icon icon="plus" />
        </button>
        <button
          type="button"
          class="answer-action-btn remove-btn ml-2"
          @click="removeAnswer"
        >
          <font-awesome-icon icon="times" />
        </button>
      </div>
    </div>
    <div
      class="answer-container mt-2"
      v-for="(answer, index) in answers"
      :key="index"
    >
      <div class="form-group mb-1">
        <div class="row">
          <div class="col-6" style="padding: 0 !important;">
            <input
              type="text"
              class="form-control"
              id="quiz-name"
              :placeholder="answer.content"
            />
          </div>
          <div class="col-6">
            <label
              ><input
                type="radio"
                name="answerRadio"
                class="mr-2"
              />Correct</label
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Question",
  data() {
    return {
      answers: []
    };
  },
  methods: {
    addAnswer() {
      this.answers.push({ content: "", is_correct: false });
    },
    removeAnswer() {
      this.answers.pop();
    }
  }
};
</script>

<style scoped>
/* Style buttons */
.answer-action-btn {
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 12px 16px; /* Some padding */
  font-size: 16px; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */
}

.add-btn {
  background-color: DodgerBlue; /* Blue background */
}

.add-btn:hover {
  background-color: RoyalBlue;
}

.remove-btn {
  background-color: red;
}

.remove-btn:hover {
  background-color: brown;
}
</style>
