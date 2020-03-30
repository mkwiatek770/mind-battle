import router from "@/router";
import userService from "../../services/userService";

const state = {
  status: localStorage.getItem("status") || "",
  username: localStorage.getItem("username") || "",
  accessToken: localStorage.getItem("accessToken") || "",
  refreshToken: localStorage.getItem("refreshToken") || ""
};

const actions = {
  login({ dispatch, commit }, { username, password }) {
    commit("loginRequest", { username });
    userService.login(username, password).then(
      userData => {
        commit("loginSuccess", userData);
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
        console.log(user);
        commit("registerSuccess", user);
        router.push("/start");
        setTimeout(() => {
          dispatch("alert/success", "Registration successful", { root: true });
        });
      },
      error => {
        console.log(error);
        commit("registerFailure", error);
        dispatch("alert/error", error, { root: true });
      }
    );
  }
};

const mutations = {
  loginRequest(state, userData) {
    state.status = { loggingIn: true };
    state.username = userData.username;
  },
  loginSuccess(state, userData) {
    state.status = { loggedIn: true };
    state.accessToken = userData.access;
    state.refreshToken = userData.refresh;
  },
  loginFailure(state) {
    state.status = {};
    state.username = "";
    state.accessToken = "";
    state.refreshToken = "";
  },
  logout(state) {
    state.status = {};
    state.username = "";
    state.accessToken = "";
    state.refreshToken = "";
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
