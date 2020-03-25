<template>
  <nav id="start-nav">
    <LoginForm />
    <LoginButton />
  </nav>
</template>

<script>
import LoginButton from "./LoginButton.vue";
import LoginForm from "./LoginForm.vue";

export default {
  name: "TheNavbar",
  components: {
    LoginForm,
    LoginButton
  },
  data: () => {}
};
</script>

<style scoped>
#start-nav {
  height: 50px;
  background-color: rgb(69, 21, 172);
  width: 100%;
}
</style>
