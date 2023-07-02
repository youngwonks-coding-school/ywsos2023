<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="main-container d-flex flex-column justify-content-between">
    <Navbar />
    <RouterView />
    <Footer />
  </div>
</template>

<script>
import { useIdle } from '@vueuse/core';
import { watch } from 'vue';
import axios from 'axios';

export default {
  data(){
    return {
      idle: null,
      sessionLifetime: null,
    }
  },
  mounted() {
    //TODO: Note working (log user out if idle for this.session_lifetime)

    // if (localStorage.getItem("accessToken")) {
    //   this.fetchSessionLifetime()
    //     .then(() => {
    //       this.setupIdleTimer();
    //     });
    // }
  },
  methods: {
    async fetchSessionLifetime() {
      try {
        const response = await this.axiosInstance.get('/api/auth/session_lifetime');
        this.sessionLifetime = response.data.session_lifetime;
      } catch (error) {
        console.log("Error fetching session lifetime:", error);
      }
    },
    logout() {
      this.axiosInstance.post('/api/auth/logout')
        .then(() => {
          localStorage.removeItem('accessToken');
          window.location.reload();
          this.$router.push({ name: 'Login' });
        })
    },
    setupIdleTimer() {
      console.log(this.sessionLifetime);
      const { idle, lastActive, reset } = useIdle(this.sessionLifetime * 1000); // Create the idle timer
      this.idle = idle; // Store the idle value in the component's data property
      watch(idle, (idleValue) => {
        if (idleValue) {
          //user is idle
          if (localStorage.getItem('accessToken')) {
            this.logout();
          }
          reset(); // Restart the idle timer
        }
      });
    },
    logout(){
      this.axiosInstance.get('/api/auth/logout', {
      headers: {Authorization: `Bearer ${localStorage.getItem('accessToken')}`}}).catch((error) => {console.log(error, "logging out");
      }).then(() => {
        localStorage.removeItem('accessToken');
        window.location.reload();
        this.$router.push('/login')
        this.idle = false;
      })
    }
  },

};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Inter:wght@300&display=swap');
body {
  font-family: 'Roboto', sans-serif;
}
</style>
