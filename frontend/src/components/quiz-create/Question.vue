<template>
  <div class="question mt-3" style="border-bottom: 1px solid black;">
    <div class="form-group mb-3">
      <label for="quiz-name">Question</label>
      <input type="text" class="form-control" id="quiz-name" placeholder="" />
    </div>

    <div class="form-group mb-3">
      <label for="quiz-name">Explaination</label>
      <input type="text" class="form-control" id="quiz-name" placeholder="" />
    </div>

    <div class="row">
      <div class="col-4"><h5>Answers</h5></div>
      <div class="col-8"><i class="fas fa-plus"></i></div>
    </div>
    <div
      class="answer-container mt-2"
      v-for="(answer, index) in answers"
      :key="index"
    >
      <div class="form-group mb-1">
        <div class="row">
          <div class="col-6">
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
    <button type="button" class="btn btn-success" @click="addAnswer">
      Add answer
    </button>
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
    }
  }
};
</script>
