<template>
  <nav id="home-nav" class="navbar justify-content-between">
    <router-link to="/" class="navbar-brand">Mind Battle</router-link>
    <div>
      <span
        >Logged in as <span class="font-weight-bold">{{ username }}</span></span
      >
      <button class="btn btn-outline-danger ml-3" @click="logout">
        Logout
      </button>
    </div>
  </nav>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "TheNavbar",
  computed: {
    ...mapState("user", ["username"])
  },
  methods: {
    ...mapActions("user", ["logout"])
  }
};
</script>

<style scoped>
#home-nav {
  height: 50px;
  width: 100%;
  border-bottom: 2px solid black;
  background-color: rgba(234, 234, 234, 0.5);
}
</style>
