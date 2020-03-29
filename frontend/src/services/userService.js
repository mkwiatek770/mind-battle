import api from "@/services/api";

export default {
  login,
  logout,
  register,
  refreshToken
};

const API_BASE_URL = "http://localhost:8000/api/v1";

function login(username, password) {
  const requestOptions = {
    headers: { "Content-Type": "application/json" },
    data: { username, password }
  };

  return api
    .post(`${API_BASE_URL}/auth/login/`, requestOptions)
    .then(handleResponse)
    .then(tokens => {
      // login successful if there's a jwt token in the response
      if (tokens.access && tokens.refresh) {
        // store user details and jwt token in local storage to keep user logged in between page refreshes
        let userObj = {
          username: username,
          access: tokens.access,
          refresh: tokens.refresh
        };
        localStorage.setItem("user", JSON.stringify(userObj));
      }

      return tokens;
    });
}

function logout() {
  // remove user from localStorage
  localStorage.removeItem("user");
}

function register(user) {
  const requestOptions = {
    headers: { "Content-Type": "application/json" },
    data: user
  };

  return api.post(`/auth/create-account/`, requestOptions).then(handleResponse);
}

function refreshToken(refresh) {
  const requestOptions = {
    headers: { "Content-Type": "application/json" },
    data: { refresh: refresh }
  };

  return api
    .post(`/auth/token/refresh/`, requestOptions)
    .then(handleResponse)
    .then(token => {
      if (token.access) {
        localStorage.setItem("accessToken", JSON.stringify(token.access));
      }
    });
}

function handleResponse(response) {
  return response.text().then(text => {
    const data = text && JSON.parse(text);
    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 response returned from api
        logout();
        location.reload(true);
      }

      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
