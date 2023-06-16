<template>
  <div class="container card col-10 col-sm-8 col-md-6 col-lg-4">
    <div class="card-body">
      <h5 class="card-title text-center">Register</h5>
      <form>
        <div class="mb-3">
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
        <div class="text-center">
          <button type="button" @click="register()" class="btn btn-primary">Register</button><br />
          <br />
          <label class="form-check-label"><a href="/login">Login</a> </label>
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
      password: ''
    }
  },
  mounted() {},
  methods: {
    register() {
      console.log('login', this.email, this.password)
      axios
        .post('/api/auth/register', { email: this.email, password: this.password })
        .then((response) => {
          console.log(response.data.message)
          this.$toast.success(response.data.message)
          this.$router.push('/login')
        })
        .catch((error) => {
          console.log(error)
          this.$toast.error(error.message)
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
