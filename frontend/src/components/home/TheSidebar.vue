<template>
  <div id="sidebar">
    <SearchQuiz />
    <CategoryList />
  </div>
</template>

<script>
import SearchQuiz from "./SearchQuiz.vue";
import CategoryList from "./CategoryList.vue";

export default {
  name: "TheSidebar",
  components: {
    SearchQuiz,
    CategoryList
  }
};
</script>

<style scoped>
#sidebar {
  background-color: purple;
  height: 100%;
}
</style>
