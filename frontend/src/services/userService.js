import api from "@/services/api";

export default {
  login,
  logout,
  register,
  refreshToken
};

function login(username, password) {
  const requestOptions = {
    url: `/auth/login/`,
    method: "POST",
    headers: { "Content-Type": "application/json" },
    data: { username, password }
  };

  return api(requestOptions)
    .then(handleResponse)
    .then(tokens => {
      // login successful if there's a jwt token in the response
      return tokens;
    });
}

function logout() {
  // remove user from localStorage
  localStorage.removeItem("user");
}

function register(user) {
  const requestOptions = {
    url: `/auth/create-account/`,
    method: "POST",
    headers: { "Content-Type": "application/json" },
    data: user
  };

  return api(requestOptions).then(handleResponse);
}

function refreshToken(refresh) {
  const requestOptions = {
    url: `/auth/token/refresh/`,
    method: "POST",
    headers: { "Content-Type": "application/json" },
    data: { refresh: refresh }
  };

  return api(requestOptions)
    .then(handleResponse)
    .then(tokens => {
      if (tokens.access) {
        localStorage.setItem("accessToken", JSON.stringify(tokens.access));
      }
    });
}

function handleResponse(response) {
  const data = response.data;
  if (response.status != 200 || response.status != 201) {
    if (response.status === 401) {
      // auto logout if 401 response returned from api
      logout();
      location.reload(true);

      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }
  }
  return data;
}
