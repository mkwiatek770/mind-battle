<template>
  <div id="register-form">
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username-input">Username</label>
        <input
          type="text"
          class="form-control"
          id="username-input"
          placeholder="Enter username"
          v-model="user.username"
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
          v-model="user.email"
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
          v-model="user.password"
        />
      </div>

      <div class="form-group">
        <label for="re-password-input">Confirm Password</label>
        <input
          type="password"
          class="form-control"
          id="re-password-input"
          v-model="user.re_password"
        />
      </div>

      <div class="form-group">
        <label for="age-input">Age</label>
        <input
          type="number"
          class="form-control"
          id="age-input"
          v-model.number="user.age"
        />
      </div>
      <div class="button-holder">
        <button type="submit" class="btn btn-success">Register</button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "Home",
  data() {
    return {
      user: {
        username: "",
        email: "",
        password: "",
        re_password: "",
        age: null
      },
      submitted: false
    };
  },
  computed: {
    ...mapState("user", ["status"])
  },
  methods: {
    ...mapActions("user", ["register"]),
    handleSubmit() {
      this.submitted = true;
      // this.$validator.validate().then(valid => {
      //   if (valid) {
      //     this.register(this.user);
      //   }
      // });
      this.register(this.user);
    }
  },
  watch: {
    status(value) {
      console.log(value);
      if (value.registerSuccess) {
        this.$emit("registeredSuccessfuly");
        this.$store.status = {};
      } else if (value.registerFailed) {
        console.log("Handle failure");
      }
    }
  }
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
