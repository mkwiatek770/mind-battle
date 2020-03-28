<template>
  <div id="category-list">
    <p style="border-bottom: 1px solid black" class="mt-5">FILTER CATEGORIES</p>

    <div
      class="d-inline-block py-1"
      v-for="category in categories"
      :key="category.id"
    >
      <a style="cursor:pointer;" class="bg-dark text-white p-1 mr-1 my-1">{{
        category.name
      }}</a>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "CategoryList",
  data() {
    return {};
  },
  computed: mapState({
    categories: state => state.quiz.categories
  }),
  methods: mapActions("categories", ["getCategories"]),
  created() {
    this.$store.dispatch("quiz/getCategories");
  }
};
</script>
