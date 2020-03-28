import quizAPI from "../../libs/quizAPI";
import categoryAPI from "../../libs/categoryAPI";

const state = {
  quizzes: [],
  categories: []
};

const getters = {
  quizzes: state => {
    return state.quizzes;
  },
  categories: state => {
    return state.categories;
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
  }
  //   getMessages({ commit }) {
  // quizAPI.fetchMessages().then(messages => {
  //   commit("setMessages", messages);
  // });
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
