<template>
  <nav class="navbar navbar-expand-md d-flex justify-content-center navbar-floating" :class="{ 'dark-theme': isDarkTheme }">
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
            <a class="nav-link" href="/dashboard" >Dashboard</a>
          </li>
          <li class="nav-item">
            <button class="nav-link" @click="changeTheme()">
              <i v-if="isDarkTheme" class="fas fa-moon"></i>
              <i v-else class="fas fa-sun"></i>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: localStorage.hasOwnProperty('accessToken'),
      isDarkTheme: true,
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('accessToken');
      this.isLoggedIn = false;
      console.log('Logged out');
    },
    changeTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      if (this.isDarkTheme) {
        localStorage.setItem('theme', 'dark');
        document.documentElement.setAttribute('data-theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');

      }
    },
  },
};
</script>
