<template>
  <div>
    <div class="meter">
      <span v-bind:style="{ width: getPercentage() }">{{
        getPercentage()
      }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProgressBar",
  props: { questionsDone: Number, totalQuestions: Number },
  methods: {
    getPercentage() {
      var percentage = Math.round(
        100 * (this.questionsDone / this.totalQuestions)
      );
      return `${percentage}%`;
    }
  }
};
</script>

<style scoped>
.meter {
  height: 20px; /* Can be anything */
  position: relative;
  background: #555;
  -moz-border-radius: 25px;
  -webkit-border-radius: 25px;
  border-radius: 25px;
  box-shadow: inset 0 -1px 1px rgba(255, 255, 255, 0.3);
}

.meter > span {
  display: block;
  height: 20px;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  background-color: rgb(43, 194, 83);
  background-image: linear-gradient(
    center bottom,
    rgb(43, 194, 83) 37%,
    rgb(84, 240, 84) 69%
  );
  box-shadow: inset 0 2px 9px rgba(255, 255, 255, 0.3),
    inset 0 -2px 6px rgba(0, 0, 0, 0.4);
  position: relative;
  overflow: hidden;
  text-align: center;
  line-height: 20px;
  color: white;
}
</style>
