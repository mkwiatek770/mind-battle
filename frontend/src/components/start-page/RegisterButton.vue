<template>
  <button
    class="btn btn-outline-success"
    @click="onClickButton"
    id="register-btn"
  >
    SIGN UP
  </button>
</template>

<script>
export default {
  name: "RegisterButton",
  methods: {
    onClickButton() {
      this.$emit("clicked");
    }
  }
};
</script>

<style scoped>
#register-btn {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 60px;
  font-size: 30px;
}
</style>
