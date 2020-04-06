<template>
  <div id="home-pagination">
    <nav aria-label="nav navigation" class="mx-auto">
      <ul class="pagination">
        <li v-if="quizzes.links.previous" class="page-item">
          <a class="page-link" href="#" @click.prevent="getPreviousPage"
            >Previous</a
          >
        </li>
        <li v-else class="page-item">
          <a class="page-link disabled">Previous</a>
        </li>

        <li class="page-item" v-for="index in quizzes.pages" :key="index">
          <a
            v-if="quizzes.current == index"
            class="active page-link"
            style="background-color: lightblue;"
            >{{ quizzes.current }}</a
          >
          <a
            v-else
            @click.prevent="getPage(index)"
            class="page-link"
            href="#"
            >{{ index }}</a
          >
        </li>

        <li v-if="quizzes.links.next" class="page-item">
          <a class="page-link" href="#" @click.prevent="getNextPage">Next</a>
        </li>
        <li v-else class="page-item">
          <a class="page-link disabled" href="">Next</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ThePagination",
  computed: {
    ...mapState("quiz", ["quizzes"]),
  },
};
</script>

<style scoped>
#home-pagination {
  width: 100%;
}

nav {
  width: 40%;
}

a.disabled {
  /* Make the disabled links grayish*/
  color: gray;
  /* And disable the pointer events */
  pointer-events: none;
}
</style>
