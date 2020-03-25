<template>
  <nav id="start-nav" class="navbar justify-content-end">
    <LoginForm />
  </nav>
</template>

<script>
import LoginForm from "./LoginForm.vue";

export default {
  name: "TheNavbar",
  components: {
    LoginForm
  },
  data: () => {}
};
</script>

<style scoped>
#start-nav {
  height: 50px;
  width: 100%;
  border-bottom: 2px solid black;
  background-color: rgba(234, 234, 234, 0.5);
}
</style>
