import api from "@/libs/api";

export default {
  getQuizzes() {
    return api
      .get(`/quizzes`)
      .then(response => response.data)
      .catch(error => {
        console.log(error);
      });
  }
};
