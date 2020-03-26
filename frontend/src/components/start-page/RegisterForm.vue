<template>
  <div id="register-form">
    <form>
      <div class="form-group">
        <label for="username-input">Username</label>
        <input
          type="text"
          class="form-control"
          id="username-input"
          placeholder="Enter username"
        />
        <small id="emailHelp" class="form-text text-muted"
          >We'll never share your email with anyone else.</small
        >
      </div>
      <div class="form-group">
        <label for="email-input">Email address</label>
        <input
          type="email"
          class="form-control"
          id="email-input"
          aria-describedby="email-help"
          placeholder="Enter email"
        />
        <small id="email-help" class="form-text text-muted"
          >We'll never share your email with anyone else.</small
        >
      </div>

      <div class="form-group">
        <label for="password-input">Password</label>
        <input
          type="password"
          class="form-control"
          id="password-input"
          placeholder="Password"
        />
      </div>

      <div class="form-group">
        <label for="re-password-input">Confirm Password</label>
        <input
          type="password"
          class="form-control"
          id="re-password-input"
          placeholder="Password"
        />
      </div>

      <div class="form-group">
        <label for="age-input">Age</label>
        <input type="number" class="form-control" id="age-input" />
      </div>
      <div class="button-holder">
        <button type="submit" class="btn btn-success">Register</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "Home"
};
</script>

<style scoped>
#register-form {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60vw;
  text-align: left;
  background-color: white;
  padding: 20px;
  z-index: 1;
}

.button-holder {
  width: 100%;
  text-align: center;
  padding-top: 20px;
}

.button-holder button {
  width: 100%;
}
</style>
