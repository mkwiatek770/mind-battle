<template>
  <div id="search-quiz">
    <p style="border-bottom: 1px solid black">SEARCH QUIZ</p>
    <form class="form-inline">
      <div class="input-group">
        <input type="text" class="form-control" placeholder="Search" />
        <div class="input-group-append">
          <button class="btn btn-secondary" type="button">
            <i class="fa fa-search"></i>
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<style scoped>
.input-group {
  width: 100%;
  padding: 20px 20% 20px 0;
}

.has-search .form-control {
  padding-left: 2.375rem;
}
</style>
