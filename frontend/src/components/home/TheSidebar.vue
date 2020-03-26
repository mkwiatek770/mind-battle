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
  padding-top: 20px;
  background-color: purple;
  height: 100vh;
  overflow-x: hidden;
  position: sticky;
  top: 0;
}
</style>
