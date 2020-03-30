import router from "@/router";
import userService from "../../services/userService";

const state = {
  status: localStorage.getItem("status") || "",
  username: localStorage.getItem("username") || "",
  accessToken: localStorage.getItem("accessToken") || "",
  refreshToken: localStorage.getItem("refreshToken") || ""
};

const getters = {
  username: state => {
    return state.username;
  }
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
    router.push("/start");
  },
  register({ dispatch, commit }, user) {
    commit("registerRequest");

    userService.register(user).then(
      user => {
        commit("registerSuccess", user);
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
    state.status = { registerSuccess: true };
    console.log("sukces");
    console.log(state.status);
  },
  registerFailure(state) {
    state.status = { registerFailed: true };
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
