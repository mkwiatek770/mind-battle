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
