<template>
  <nav class="navbar navbar-expand-md bg-light d-flex justify-content-start w-100">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">YWSOS</a>
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
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if="!isLoggedIn">
            <a class="nav-link active" aria-current="page" href="/register">Register</a>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <a class="nav-link" href="/login">Login</a>
          </li>
          <li class="nav-item" v-else>
            <a class="nav-link" href="#" @click="logout">Logout</a>
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
      isLoggedIn: localStorage.hasOwnProperty("accessToken"),
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("accessToken");
      this.isLoggedIn = false;
      console.log("Logged out")
    },
  },
};
</script>
