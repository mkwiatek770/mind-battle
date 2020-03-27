<template>
  <div id="quiz-detail">
    <TheNavbar />
    <div class="row">
      <div
        id="question-element"
        class="col-sm-9 col-md-8 col-lg-6 col-xl-5 mx-auto mt-5 p-5"
        style="background-color: white"
      >
        <TheHeader :name="quiz.name" />
        <ProgressBar
          :questionsDone="questionsDone"
          :totalQuestions="questions.length"
        />
        <Question :question="questions[currentQuestionIndex]" />
      </div>
    </div>
  </div>
</template>

<script>
import TheNavbar from "@/components/quiz-detail/TheNavbar.vue";
import TheHeader from "@/components/quiz-detail/TheHeader.vue";
import ProgressBar from "@/components/quiz-detail/ProgressBar.vue";
import Question from "@/components/quiz-detail/Question.vue";

export default {
  name: "QuizDetail",
  components: {
    TheNavbar,
    TheHeader,
    ProgressBar,
    Question
  },
  data() {
    return {
      questionsDone: 0,
      currentQuestionIndex: 0,
      quiz: {
        name: "Quiz 1"
      },
      questions: [
        {
          question: "What is your name?",
          answers: [
            {
              id: 4397,
              content: "bew one",
              is_correct: false
            },
            {
              id: 4398,
              content: "second",
              is_correct: true
            }
          ],
          explaination: "Lorem ipsum ffff..."
        },
        {
          question: "Second one?",
          answers: [
            {
              id: 4397,
              content: "python",
              is_correct: false
            },
            {
              id: 4398,
              content: "nie wiem",
              is_correct: true
            }
          ],
          explaination: "Lorem ipsum ffff..."
        },
        {
          question: "What is your name?",
          answers: [
            {
              id: 4397,
              content: "bew one",
              is_correct: false
            },
            {
              id: 4398,
              content: "second",
              is_correct: true
            }
          ],
          explaination: "Lorem ipsum ffff..."
        }
      ]
    };
  }
};
</script>

<style scoped>
#quiz-detail {
  width: 100%;
  height: 100vh;
}

#question-element {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
