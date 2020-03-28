<template>
  <form class="form-inline align-middle" id="login-form">
    <div class="form-group mx-sm-3 mb-2">
      <label for="input-username" class="sr-only">Username</label>
      <input
        type="text"
        class="form-control"
        id="input-username"
        placeholder="Username"
        v-model="username"
      />
    </div>
    <div class="form-group mx-sm-3 mb-2">
      <label for="input-password" class="sr-only">Password</label>
      <input
        type="password"
        class="form-control"
        id="input-password"
        placeholder="Password"
        v-model="password"
      />
    </div>
    <button type="button" @click="handleSubmit" class="btn btn-success mb-2">
      Login
    </button>
  </form>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "LoginForm",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    ...mapActions("user", ["login"]),
    handleSubmit() {
      const { username, password } = this;
      if (username && password) {
        this.login({ username, password });
      }
    }
  }
};
</script>
