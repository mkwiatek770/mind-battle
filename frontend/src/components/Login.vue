<template>
  <div>
    <form class="login" @submit.prevent="login">
      <h1>Sign in</h1>
      <label>User name</label>
      <input v-model="username" required type="text" placeholder="Snoopy" />
      <label>Password</label>
      <input v-model="password" required type="password" placeholder="Password" />
      <hr />
      <button type="submit" @click="login()">Login</button>
    </form>

    <p>Username: {{ username }}</p>
    <p>Password: {{ password }}</p>
  </div>
</template>


<script>
import { HTTP } from "@/services/api";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      AUTH_REQUEST: ""
    };
  },
  methods: {
    login() {
      HTTP.post("auth/login/", {
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
        .then(response => {
          console.log(response);
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>

<style scoped>
</style>
