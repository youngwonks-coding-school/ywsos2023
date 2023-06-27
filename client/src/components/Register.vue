<template>
  <div class="container card col-10 col-sm-8 col-md-6 col-lg-4">
    <div class="card-body">
      <h5 class="card-title text-center">Register</h5>
      <form>
        <div class="mb-3">
          <div class="form-group d-flex justify-content-center">
            <ul class="nav nav-tabs">
              <li class="nav-item" v-for="(option, index) in options" :key="index">
                <a class="nav-link" :class="{ active: selectedOption === option }" @click="selectOption(option)">{{ option }}</a>
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
            :class="{ 'is-invalid': !isValidPassword, 'is-valid': isValidPassword }"
            required
          />
        </div>
        <div class="mb-3 form-check">
          <input type="checkbox" class="form-check-input" id="terms-privacy-check" />
          <label class="form-check-label" for="terms-privacy-check"
            >I agree to the <a href="/terms-of-service">terms of servcie</a> and
            <a href="/privacy-policy">privacy policy</a></label
          >
        </div>
        <div class="text-center mt-3">
          <button type="button" @click="register()" class="btn btn-primary form-button">Register</button><br />
          <br />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      email: '',
      password: '',
      options: ['Restaurant', 'Food Bank'],
      selectedOption: 'Restaurant'
    }
  },
  methods: {
    selectOption(option) {
      this.selectedOption = option;
    },
    register() {
      console.log('login', this.email, this.password)
      axios
        .post('/api/auth/register', { email: this.email, password: this.password, business_type: this.selectOption })
        .then((response) => {

          this.$toast.success(response.data.message)
          localStorage.setItem('accessToken', response.data.access_token)
          localStorage.setItem('refreshToken', response.data.refresh_token)

          this.$router.push('/profile');
          setTimeout(() => {
            window.location.reload();
          }, 10);
        })
        .catch((error) => {
          console.log(error)
          this.$toast.error(error.response)
        })
    }
  },
  computed: {
    isValidEmail() {
      const emailRegex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/
      return emailRegex.test(this.email)
    },
    isValidPassword() {
      return this.password.length >= 8
    }
  }
}
</script>

<style scoped>
  .nav-item{
    cursor: pointer;

  }

  .nav-link.active {
    background-color: rgb(255,255,255, 0);
    border: .5px solid black;
}
</style>