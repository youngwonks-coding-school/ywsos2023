<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import { socket, state } from "./socket.js";
import { onMounted } from 'vue';


onMounted(() => {
  socket.connect();
});
</script>

<template>
  <div class="main-container d-flex flex-column justify-content-between">
    <Navbar />
    <RouterView />
    <Footer />
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Inter:wght@300&display=swap');
body {
  font-family: 'Roboto', sans-serif;
}
</style>
