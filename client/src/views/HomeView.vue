<template>
    <div class="home-container">
      <div class="vector1">
        <img src="../../public/images/path1.svg" alt="vector1" />
      </div>
      <div class="d-flex flex-column align-items-start home-ts">
        <h1 class="home-title">Walk Wise</h1>
        <h2 class="home-subtitle">Step into Serenity: Discover, Rate, and Share Inspiring Walking Routes</h2>
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