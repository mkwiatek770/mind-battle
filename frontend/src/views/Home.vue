<template>
  <div class="home">
    <TheNavbar />
    <div class="row">
      <div class="col-sm-12 col-md-8 col-lg-9">
        <TheMain />
        <ThePagination />
      </div>
      <div class="col-sm-12 col-md-4 col-lg-3">
        <TheSidebar />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import TheNavbar from "@/components/base/TheNavbar.vue";
import TheMain from "@/components/home/TheMain.vue";
import TheSidebar from "@/components/home/TheSidebar.vue";
import ThePagination from "@/components/home/ThePagination.vue";

export default {
  name: "Home",
  components: {
    TheNavbar,
    TheMain,
    TheSidebar,
    ThePagination,
  },
};
</script>

<style scoped>
#start {
  width: 100%;
  height: 100vh;
}

div.row div {
  padding: 0px;
}
</style>
