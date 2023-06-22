<template>
    <div class="home-container">
      <div class="home-truck">
        <img src="../../public/images/truck.png" alt="truck" />
      </div>
      <div class="d-flex flex-column align-items-start home-ts">
        <h1 class="home-title">Yum Union</h1>
        <h2 class="home-subtitle">Wasting None, Feeding Everyone!"</h2>
      </div>
    <div class="d-flex flex-column home-auth">
        <router-link  v-if="loggedOut" to="/register" class="btn btn-secondary button mb-3 ">Register</router-link>
        <router-link  v-if="loggedOut" to="/login" class="btn btn-secondary button">Login</router-link>
    </div>

    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        loggedOut: true
      };
    },
    mounted() {
      // Check if 'accessToken' exists in localStorage
      const accessToken = localStorage.getItem('accessToken');
      if (accessToken) {
        this.loggedOut = false;
      }
      else {
        this.loggedOut = true;
      }
    }
  };
  </script>