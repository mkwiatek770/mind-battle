import userAPI from "../../libs/userAPI";

const state = {
  username: "",
  accessToken: "",
  refreshToken: ""
};

const getters = {
  username: state => {
    return state.username;
  },
  accessToken: state => {
    return state.accessToken;
  },
  refreshToken: state => {
    return state.refreshToken;
  }
};

const actions = {
  login({ commit }, username, password) {
    var loginData = {
      username: username,
      password: password
    };
    userAPI.login(loginData).then(tokens => {
      commit("setTokens", tokens);
    });
  }
};

const mutations = {
  setTokens(state, tokens) {
    state.accessToken = tokens.access;
    state.refreshToken = tokens.refresh;
  },
  setUsername(state, username) {
    state.username = username;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
