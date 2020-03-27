<template>
  <div>
    <h1>{{ name }}</h1>
  </div>
</template>

<script>
export default {
  name: "TheHeader",
  props: {
    name: String
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  font-weight: bold;
  padding-bottom: 20px;
}
</style>
