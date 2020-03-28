import axios from "axios";
import Cookies from "js-cookie";

export default axios.create({
  baseURL: "http://localhost:8000/api/v1",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken")
  }
});

// Poradnik na podstawie którego pisać kod
// https://jasonwatmore.com/post/2018/07/14/vue-vuex-user-registration-and-login-tutorial-example

// ##############################
// zrobione
// ##############################

// /quizzes/ GET
// /categories/ GET, POST

// ##############################
// endpointy do zaimplementowania
// ##############################

// /auth/login/ POST
// /auth/create-account/ POST
// /auth/token/refresh/ POST
// /auth/logout/ POST
// /quizzes/ POST, GET(filtrowanie)
// /categories/ POST, DELETE
// /quizzes/drafts/ GET
// /quizzes/<id>/avatar/ GET, PUT, DELETE
// /quizzes/<id>/publish/ POST
// /quizzes/<id>/unpublish/ POST
// /quizzes/<id>/ GET, PUT, DELETE
// /quizzes/<id>/questions/ GET, POST
// /quizzes/<id>/questions/<id>/ PUT, DELETE
// /quizzes/<id>/questions/<id>/answer PUT
// quizzes/<id>/publish/ POST
// /quizzes/<id>/unpublish/ POST
// /quizzes/<id>/image/ GET, PUT, DELETE
