import api from "@/libs/api";

export default {
  login(data) {
    return api
      .post(`/auth/login`, {
        body: JSON.stringify(data)
      })
      .then(response => response.data)
      .catch(error => {
        console.log(error);
      });
  },
  createAccount(data) {
    return api
      .post(`/auth/create-account`, {
        body: JSON.stringify(data)
      })
      .then(response => response.data)
      .catch(error => {
        console.log(error);
      });
  },
  refreshToken() {
    return api
      .post(`/auth/token/refresh`, {
        body: JSON.stringify(data)
      })
      .then(response => response.data)
      .catch(error => {
        console.log(error);
      });
  }
};
