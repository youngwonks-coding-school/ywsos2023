<template>
  <div class="d-flex flex-grow-1 align-self-center justify-content-center flex-column">
    YWSOS2023 Dashboard
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
    verifyUserSession() {
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
          console.log(response.data.message)
          this.$toast.success('Already Logged in.')
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
            })
            .catch((error) => {
              console.log(error)
              localStorage.removeItem('refreshToken')
              localStorage.removeItem('accessToken')
              this.$router.push('/login')

              this.$toast.error(error.response.data.msg)
            })
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
