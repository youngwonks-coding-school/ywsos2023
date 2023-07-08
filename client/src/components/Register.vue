<template>
  <div class="container card col-10 col-sm-8 col-md-6 col-lg-4">
    <div class="card-body">
      <h5 class="card-title text-center">Register</h5>
      <form>
        <div class="mb-3">
          <div class="form-group d-flex justify-content-center">
            <ul class="nav nav-tabs">
              <li
                class="nav-item"
                v-for="(option, index) in display_options"
                :key="index"
              >
              <a
              class="nav-link"
              :class="{ active: selectedOption === options[index] }"
              @click="selectOption(options[index])"
              >
                {{ option }}
              </a>
              </li>
            </ul>
          </div>
          <label for="email" class="form-label">Email address</label>
          <input
            type="text"
            class="form-control"
            id="email"
            v-model="email"
            :class="{ 'is-invalid': !isValidEmail, 'is-valid': isValidEmail }"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            autocomplete="on"
            v-model="password"
            :class="{
              'is-invalid': !isValidPassword,
              'is-valid': isValidPassword,
            }"
            required
          />
        </div>
        <div class="mb-3 form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="terms-privacy-check"
          />
          <label class="form-check-label" for="terms-privacy-check"
            >I agree to the <a href="/terms-of-service">terms of servcie</a> and
            <a href="/privacy-policy">privacy policy</a></label
          >
        </div>
        <div class="text-center">
          <button
            type="button"
            @click="register()"
            class="btn btn-primary form-button mt-4"
            id="register"
            :disabled="!isValidEmail || !isValidPassword || !email || !password"
          >
            Register</button
          ><br />
          <br />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      email: "",
      password: "",
      display_options: ["Restaurant", "Food Bank"],
      options: ["restaurant", "food_bank"],
      selectedOption: "restaurant",
    };
  },
  methods: {
    //set the business type on tab change (restaurant or food bank)
    selectOption(option) {
      this.selectedOption = option;
    },

    //register the user (send business type in addition to email and password)
    register() {

      localStorage.setItem("business_type", this.selectedOption);
      console.log("Registering email: "+ this.email +" business type", this.selectedOption);
      axios
        .post("/api/auth/register", {
          email: this.email,
          password: this.password,
          business_type: this.selectedOption,
        })
        .then((response) => {
          localStorage.setItem("accessToken", response.data.access_token);
          localStorage.setItem("refreshToken", response.data.refresh_token);

          //dispatch custom event to update the localstorage in the navbar
          window.dispatchEvent(new CustomEvent('access-token-localstorage-changed', {
            detail: {
              storage: localStorage.getItem('accessToken')
            }
          }));

          this.$toast.success(response.data.message);
          this.$router.push('/profile')

          
        })
        .catch((error) => {
          console.log("Error Registering", error.response.data.message);
          this.$toast.error(error.response.data.message);
        });
    },
  },
  computed: {
    isValidEmail() {
      const emailRegex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
      return emailRegex.test(this.email);
    },
    isValidPassword() {
      return this.password.length >= 8;
    },
  },
};
</script>

<style scoped>
.nav-item {
  cursor: pointer;
}

.nav-link.active {
  background-color: rgb(255, 255, 255, 0);
  border: 0.5px solid black;
}
</style>
