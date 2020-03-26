<template>
  <div class="home">
    <TheNavbar />
    <TheMain />
    <TheSidebar />
  </div>
</template>

<script>
// @ is an alias to /src
import TheNavbar from "@/components/home/TheNavbar.vue";
import TheMain from "@/components/home/TheMain.vue";
import TheSidebar from "@/components/home/TheSidebar.vue";

export default {
  name: "Home",
  components: {
    TheNavbar,
    TheMain,
    TheSidebar
  }
};
</script>
