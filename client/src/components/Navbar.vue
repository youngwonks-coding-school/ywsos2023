<template>
  <nav class="navbar navbar-expand-md d-flex justify-content-center navbar-floating">
    <div class="navbar-header">
        <a class="navbar-brand" href="/">YWSOS</a>
    </div>
    <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mb-2 mb-lg-0">
          <li class="nav-item" v-if="!isLoggedIn">
            <a class="nav-link" aria-current="page" href="/register">Register</a>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <a class="nav-link" href="/login">Login</a>
          </li>
          <li class="nav-item" v-else>
            <a class="nav-link" href="/logout" @click="logout">Logout</a>
          </li>
          <li class="nav-item" id="clock">
            <span class="clock-text">{{ currentTime }}</span>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import moment from 'moment-timezone'; // Import moment-timezone library

export default {
  data() {
    return {
      isLoggedIn: localStorage.hasOwnProperty('accessToken'),
    };
  },
  computed: {
    currentTime() {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const format = 'HH:mm:ss'; // Format for displaying time
      return moment().tz(timezone).format(format);
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('accessToken');
      this.isLoggedIn = false;
      console.log('Logged out');
    },
    updateClock() {
      this.$el.querySelector('.clock-text').textContent = this.currentTime;
    },
  },
  mounted() {
    this.updateClock(); 

    setInterval(() => {
      this.updateClock();
    }, 1000);
  },
};
</script>