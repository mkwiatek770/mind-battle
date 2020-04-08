import axios from "axios";
import Cookies from "js-cookie";
import store from "@/store";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
  },
});

api.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    // Return any error which is not due to authentication back to the calling service
    // if (error.response.status !== 401){
    //   return new Promise((resolve, reject) => {
    //     reject(error);
    //   })
    // }

    // // Logout user if token refresh didn't work or user is disabled
    // if (error.config.url == '/api/token/refresh' || error.response.message == 'Account is disabled.') {
    //   router PushManager()
    // }

    if (error.response.status === 401) {
      // Try request again with new token
      store.dispatch("refreshToken", store.refreshToken).then((token) => {
        // new request with new token
        const config = error.config;
        config.headers["Authorization"] = `Bearer ${token}`;

        return new Promise((resolve, reject) => {
          api
            .request(config)
            .then((response) => {
              resolve(response);
            })
            .catch((error) => {
              reject(error);
            });
        });
      });
    }

    return new Promise((resolve, reject) => {
      reject(error);
    });
  }
);

export default api;

// export const authenticationHeader = () => {
//   return {
//     Authorization: `Bearer ${Auth.getAccessToken()}`
//   };
// };
