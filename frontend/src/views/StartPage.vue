<template>
  <div id="start">
    <TheNavbar />
    <RegisterForm v-if="isRegisterBtnClicked" />
    <RegisterButton @clicked="isRegisterBtnClicked = true" />
  </div>
</template>

<script>
import RegisterButton from "@/components/start-page/RegisterButton.vue";
import RegisterForm from "@/components/start-page/RegisterForm.vue";
import TheNavbar from "@/components/start-page/TheNavbar.vue";

export default {
  name: "StartPage",
  components: {
    RegisterForm,
    RegisterButton,
    TheNavbar
  },
  data: () => ({
    isRegisterBtnClicked: false
  }),
  methods: {
    action() {
      console.log("dupa");
    }
  }
};
</script>

<style scoped>
#start {
  width: 100%;
  height: 100vh;
}

#start:after {
  content: "";
  background-image: url("../assets/question-bg.png");
  opacity: 0.3;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  position: absolute;
  z-index: -1;
}
</style>
