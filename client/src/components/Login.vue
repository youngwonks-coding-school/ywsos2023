<template>
  <div class="container card col-10 col-sm-8 col-md-6 col-lg-4">
    <div class="card-body">
      <h5 class="card-title text-center">Login</h5>
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
          <button type="button" @click="login()" class="btn btn-primary button" id="login">Login</button><br /><br />

          <label class="form-check-label"><a href="/register">Register</a> </label>

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
  mounted() {
    this.verifyUserSession()
  },
  methods: {
    login() {
      console.log('login', this.email, this.password)
      axios
        .post('/api/auth/login', { email: this.email, password: this.password })
        .then((response) => {
          this.$toast.success(response.data.message)
          localStorage.setItem('accessToken', response.data.access_token)
          localStorage.setItem('refreshToken', response.data.refresh_token)
          localStorage.setItem('business_type', response.data.business_type )

          window.dispatchEvent(new CustomEvent('access-token-localstorage-changed', {
            detail: {
              storage: localStorage.getItem('accessToken')
            }
          }));
          this.$router.push('/dashboard')
        })
        .catch((error) => {
          console.log(error)
          this.$toast.error(error.message)
        })
    },
    verifyUserSession() {
      console.log('verifyUserSession')
      if (localStorage.hasOwnProperty('accessToken')) {
        axios
          .post(
            '/api/auth/verify',
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('accessToken')}`
              }
            }
          )
          .then((response) => {
            this.$toast.success(response.data.message)
            this.$router.push('/dashboard')
          })
          .catch((error) => {
            console.log(error)
            this.$toast.error(error.response.data.msg)
            axios
              .post(
                '/api/auth/refresh',
                {},
                {
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('refreshToken')}`
                  }
                }
              )
              .then((response) => {
                console.log(response.data.message)
                this.$toast.success(response.data.message)
                localStorage.setItem('accessToken', response.data.access_token)

                this.$router.push('/dashboard')
              })
              .catch((error) => {
                console.log(error)
                localStorage.removeItem('refreshToken')
                localStorage.removeItem('accessToken')

                this.$toast.error(error.response.data.msg)
              })
          })
      } else {
        console.log('no access token found')
      }
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