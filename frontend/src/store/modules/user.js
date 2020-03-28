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
  login({ commit }, { username, password }) {
    console.log(`${username}, ${password}`);
    userAPI.login(username, password).then(tokens => {
      commit("setTokens", tokens);
    });
  }
};

const mutations = {
  setTokens(state, tokens) {
    state.accessToken = tokens.access;
    state.refreshToken = tokens.refresh;
    console.log("Nowe tokeny");
    console.log(state.accessToken);
    console.log(state.refreshToken);
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
