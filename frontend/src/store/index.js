import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import alert from "./modules/alert";
import quiz from "./modules/quiz";
import user from "./modules/user";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { alert, quiz, user },
  plugins: [createPersistedState()]
});
