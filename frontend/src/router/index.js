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
  },

  // otherwise redirect to home
  { path: "*", redirect: "/" }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

/*
router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})
*/

export default router;
