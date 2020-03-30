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
import { mapState, mapActions } from "vuex";

export default {
  name: "LoginForm",
  data() {
    return {
      username: "",
      password: "",
      submitted: false
    };
  },
  computed: {
    ...mapState("user", ["status"])
  },
  methods: {
    ...mapActions("user", ["login", "logout"]),
    handleSubmit() {
      this.submitted = true;
      const { username, password } = this;
      if (username && password) {
        this.login({ username, password });
      }
    }
  },
  created() {
    // reset login status
    this.logout();
  }
};
</script>
