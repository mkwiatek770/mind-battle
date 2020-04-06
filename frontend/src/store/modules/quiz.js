import router from "@/router";
import quizAPI from "../../services/quizService";
import categoryAPI from "../../services/categoryService";

const state = {
  quizzes: {},
  categories: [],
  recentQuiz: {},
  quizStarted: false,
};

const getters = {
  quizzes: (state) => {
    return state.quizzes;
  },
  categories: (state) => {
    return state.categories;
  },
  recentQuiz: (state) => {
    return state.recentQuiz;
  },
};

const actions = {
  getQuizzes({ commit }, pageNumber = 1) {
    quizAPI.getQuizzes(pageNumber).then((quizzes) => {
      commit("setQuizzes", quizzes);
    });
  },
  getCategories({ commit }) {
    categoryAPI.getCategories().then((categories) => {
      commit("setCategories", categories);
    });
  },
  getQuizWithQuestions({ dispatch, commit }, id) {
    // get quiz detail
    quizAPI.getQuizDetail(id).then((quizData) => {
      commit("setQuizData", quizData);
    });

    // get questions for quiz
    quizAPI.getQuestionsForQuiz(id).then(
      (questions) => {
        commit("setQuizQuestions", questions);
        router.push(`/quiz/${id}`);
      },
      (error) => {
        commit("responseFailure", error);
        dispatch("alert/error", error, { root: true });
        router.push("/");
      }
    );
  },
  startQuizByUser({ commit }, id) {
    commit("startQuiz");
    quizAPI.startQuiz(id);
  },
  finishQuizByUser({ commit }, data) {
    quizAPI.answerToAllQuizQuestions(data.id, data.answers).then(() => {
      quizAPI.finishQuiz(data.id).then(() => {
        commit("finishQuiz");
        router.push("/quiz/summary");
      });
    });
  },
  createQuiz({ dispatch }, { quiz, questions, image }) {
    quizAPI
      .createQuiz(quiz)
      .then((response) => {
        quizAPI.addImageToQuiz(response.id, image);

        quizAPI.addQuestionsToQuiz(response.id, questions).then(() => {
          router.push("/");
        });
      })
      .catch((error) => {
        dispatch("alert/error", error, { root: true });
      });
  },
};

const mutations = {
  setQuizzes(state, quizzes) {
    state.quizzes = quizzes;
  },
  setCategories(state, categories) {
    state.categories = categories;
  },
  setQuizData(state, quizData) {
    state.recentQuiz = quizData;
  },
  setQuizQuestions(state, questions) {
    state.recentQuiz.questions = questions;
  },
  responseFailure(state) {
    state.recentQuiz = {};
  },
  startQuiz(state) {
    state.quizStarted = true;
  },
  finishQuiz(state) {
    state.quizStarted = false;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
