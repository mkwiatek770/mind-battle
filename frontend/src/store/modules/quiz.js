import quizAPI from "../../libs/quizAPI";

const state = {
  quizzes: []
};

const getters = {
  quizzes: state => {
    return state.quizzes;
  }
};

const actions = {
  getQuizzes({ commit }) {
    quizAPI.getQuizzes().then(quizzes => {
      commit("setQuizzes", quizzes);
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
