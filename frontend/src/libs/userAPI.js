import api from "@/libs/api";

export default {
  login(username, password) {
    return api
      .post(`/auth/login/`, {
        body: JSON.stringify({ username, password }),
        headers: { "Content-Type": "application/json" }
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
  refreshToken(data) {
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
