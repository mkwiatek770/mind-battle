import api from "@/services/api";

export default {
  getQuizzes() {
    return api
      .get(`/quizzes`)
      .then(response => response.data)
      .catch(error => {
        console.log(error);
      });
  },
  getQuizDetail(id, accessToken) {
    const requestOptions = {
      url: `/quizzes/${id}`,
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      }
    };
    return api(requestOptions).then(response => response.data);
  },
  getQuestionsForQuiz(id) {
    const accessToken = JSON.parse(localStorage.vuex).user.accessToken;
    const requestOptions = {
      url: `/quizzes/${id}/questions`,
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      }
    };
    return api(requestOptions).then(response => response.data);
  }
};
