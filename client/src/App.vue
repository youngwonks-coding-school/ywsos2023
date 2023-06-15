<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="d-flex flex-column justify-content-between align-items-start min-vh-100">
    <Navbar />
    <RouterView />
    <Footer />
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Sofia');
body {
  font-family: 'Sofia', sans-serif;
}
</style>
