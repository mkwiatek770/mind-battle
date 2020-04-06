import api from "@/services/api";

export default {
  getQuizzes(pageNumber) {
    return api
      .get(`/quizzes?page=${pageNumber}`)
      .then((response) => response.data)
      .catch((error) => {
        console.log(error);
      });
  },
  getQuizDetail(id) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${id}/`,
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    };
    return api(requestOptions).then((response) => response.data);
  },
  getQuestionsForQuiz(id) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${id}/questions/`,
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    };
    return api(requestOptions).then((response) => response.data);
  },
  startQuiz(id) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${id}/start/`,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    };
    return api(requestOptions).then((response) => response.data);
  },
  finishQuiz(id) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${id}/finish/`,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    };
    return api(requestOptions).then((response) => response.data);
  },
  answerToAllQuizQuestions(id, answers) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${id}/answer/`,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      data: { answers: answers },
    };
    return api(requestOptions).then((response) => response.data);
  },
  createQuiz(quizData) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/`,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      data: quizData,
    };
    return api(requestOptions).then((response) => response.data);
  },
  addQuestionsToQuiz(quiz_id, questions) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${quiz_id}/questions/`,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      data: questions,
    };
    return api(requestOptions).then((response) => response.data);
  },
  addImageToQuiz(quiz_id, image) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${quiz_id}/image/`,
      method: "PUT",
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${accessToken}`,
      },
      data: { image: image },
    };
    return api(requestOptions).then((response) => response.data);
  },
};
