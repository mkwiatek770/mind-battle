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
  getQuizWithQuestions(id, accessToken) {
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
