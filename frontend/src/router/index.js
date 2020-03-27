import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/start",
    name: "StartPage",
    component: () => import("../views/StartPage.vue")
  },
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/quiz",
    name: "QuizDetail",
    component: () => import("../views/QuizDetail.vue")
  },
  {
    path: "/quiz/new",
    name: "QuizCreate",
    component: () => import("../views/QuizCreate.vue")
  },
  {
    path: "/quiz/edit",
    name: "QuizEdit",
    component: () => import("../views/QuizEdit.vue")
  }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

export default router;
