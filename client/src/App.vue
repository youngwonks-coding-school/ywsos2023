<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div className="main-container d-flex flex-column min-vh-100">
    <Navbar />
    <RouterView />
    <Footer />
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
body {
  font-family: 'Roboto', sans-serif;
}
</style>
