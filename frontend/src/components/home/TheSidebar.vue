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
  height: 100vh;
  border-left: 2px solid black;
  padding-left: 10px;
  overflow-x: hidden;
  position: sticky;
  top: 0;
}
</style>
