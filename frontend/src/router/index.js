// import axios from "axios";
import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
// import { Store } from "vuex";
// import store from "store";

Vue.use(VueRouter);

const routes = [
  {
    path: "/start",
    name: "StartPage",
    component: () => import("../views/StartPage.vue"),
    meta: {
      guest: true
    }
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/quiz/new",
    name: "QuizCreate",
    component: () => import("../views/QuizCreate.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/quiz/edit",
    name: "QuizEdit",
    component: () => import("../views/QuizEdit.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/quiz/solve",
    name: "QuizSolve",
    component: () => import("../views/QuizSolve.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/quiz/summary",
    name: "QuizSummary",
    component: () => import("../views/QuizSummary.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/quiz/:id",
    name: "QuizDetail",
    component: () => import("../views/QuizDetail.vue"),
    meta: {
      requiresAuth: true
    }
  },

  // otherwise redirect to home
  { path: "*", redirect: "/" }
];

// let isRefreshing = false;

// axios.interceptors.response.use(
//   response => {
//     return response;
//   },
//   error => {
//     const {
//       config,
//       response: { status, data }
//     } = error;

//     const originalRequest = config;

//     if (status === 401 && data.message == "Token is invalid or expired") {
//       if (!isRefreshing) {
//         isRefreshing = true;
//         store
//           .dispatch("refreshToken")
//           .then(({ status }) => {
//             if (status === 200 || status === 204) {
//               isRefreshing = false;
//             }
//           })
//           .catch(error => {
//             console.error(error);
//           });
//       }
//     }
//   }
// );

const router = new VueRouter({
  routes,
  mode: "history"
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!JSON.parse(localStorage.vuex).user.accessToken) {
      next({
        path: "/start",
        params: { nextUrl: to.fullPath }
      });
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.guest)) {
    next();
  }
  next();
});

export default router;
