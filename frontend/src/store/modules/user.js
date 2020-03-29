import router from "vue-router";
import userService from "../../services/userService";

const user = JSON.parse(localStorage.getItem("user"));
const state = {
  user: user
    ? { status: { loggedIn: true }, user }
    : { status: {}, user: null },
  accessToken: "",
  refreshToken: ""
};

const actions = {
  login({ dispatch, commit }, { username, password }) {
    commit("loginRequest", { username });

    userService.login(username, password).then(
      user => {
        commit("loginSuccess", user);
        router.push("/");
      },
      error => {
        commit("loginFailure", error);
        dispatch("alert/error", error, { root: true });
      }
    );
  },
  logout({ commit }) {
    userService.logout();
    commit("logout");
  },
  register({ dispatch, commit }, user) {
    commit("registerRequest");

    userService.register(user).then(
      user => {
        commit("registerSuccess", user);
        router.push("/start");
        setTimeout(() => {
          dispatch("alert/success", "Registration successful", { root: true });
        });
      },
      error => {
        commit("registerFailure", error);
        dispatch("alert/error", error, { root: true });
      }
    );
  }
};

const mutations = {
  loginRequest(state, user) {
    state.status = { loggingIn: true };
    state.user = user;
  },
  loginSuccess(state, user) {
    state.status = { loggedIn: true };
    state.user = user;
  },
  loginFailure(state) {
    state.status = {};
    state.user = null;
  },
  logout(state) {
    state.status = {};
    state.user = null;
  },
  registerRequest(state) {
    state.status = { registering: true };
  },
  registerSuccess(state) {
    state.status = {};
  },
  registerFailure(state) {
    state.status = {};
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
