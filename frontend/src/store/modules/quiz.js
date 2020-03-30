import router from "@/router";
import quizAPI from "../../services/quizService";
import categoryAPI from "../../services/categoryService";

const state = {
  quizzes: [],
  categories: [],
  recentQuiz: {}
};

const getters = {
  quizzes: state => {
    return state.quizzes;
  },
  categories: state => {
    return state.categories;
  },
  recentQuiz: state => {
    return state.recentQuiz;
  }
};

const actions = {
  getQuizzes({ commit }) {
    quizAPI.getQuizzes().then(quizzes => {
      commit("setQuizzes", quizzes);
    });
  },
  getCategories({ commit }) {
    categoryAPI.getCategories().then(categories => {
      commit("setCategories", categories);
    });
  },
  getQuizWithQuestions({ dispatch, commit }, id) {
    // get quiz detail
    quizAPI.getQuizDetail(id).then(quizData => {
      console.log(quizData);
      commit("setQuizData", quizData);
    });

    // get questions for quiz
    quizAPI.getQuestionsForQuiz(id).then(
      questions => {
        commit("setQuizQuestions", questions);
        router.push(`/quiz/${id}`);
      },
      error => {
        commit("responseFailure", error);
        dispatch("alert/error", error, { root: true });
        router.push("/");
      }
    );
  }

  //   },
  //   addMessage({ commit }, message) {
  // quizAPI.postMessage(message).then(() => {
  //   commit("addMessage", message);
  // });
  //   },
  //   deleteMessage({ commit }, msgId) {
  // quizAPI.deleteMessage(msgId);
  // commit("deleteMessage", msgId);
  //   }
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
  }

  // addMessage(state, message) {
  //   state.messages.push(message)
  // },
  // deleteMessage(state, msgId) {
  //   state.messages = state.messages.filter(obj => obj.pk !== msgId)
  // }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
