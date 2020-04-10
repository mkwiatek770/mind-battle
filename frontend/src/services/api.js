import axios from "axios";
import Cookies from "js-cookie";
import store from "@/store";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken")
  }
});

api.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    if (error.response.status !== 401) {
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }

    // Logout user if token refresh didn't work
    if (error.config.url === "/auth/token/refresh/") {
      localStorage.removeItem("user");
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }

    if (store.getters["user/refreshToken"]) {
      // Try request again with new token
      store
        .dispatch("user/refreshToken", store.getters["user/refreshToken"])
        .then(() => {
          // new request with new token
          const config = error.config;
          const token = localStorage.getItem("refreshToken");
          config.headers["Authorization"] = `Bearer ${token}`;

          return new Promise((resolve, reject) => {
            axios
              .request(config)
              .then(response => {
                resolve(response);
              })
              .catch(error => {
                reject(error);
              });
          });
        })
        .catch(error => {
          return new Promise((resolve, reject) => {
            reject(error);
          });
        });
    } else {
      return new Promise((resolve, reject) => {
        reject(error);
      });
    }
  }
);

export default api;

// export const authenticationHeader = () => {
//   return {
//     Authorization: `Bearer ${Auth.getAccessToken()}`
//   };
// };
