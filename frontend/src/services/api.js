import axios from "axios";
import Cookies from "js-cookie";

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
    console.log("Git");
    console.log(response);
    return response;
  },
  function(error) {
    console.log("Err");
    console.log(error);
  }
);

export default api;

// export const authenticationHeader = () => {
//   return {
//     Authorization: `Bearer ${Auth.getAccessToken()}`
//   };
// };
