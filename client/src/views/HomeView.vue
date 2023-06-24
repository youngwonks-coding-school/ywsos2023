<template>
    <div class="home-container">
      <div class="first-container d-flex justify-content-center">
        <h1 class="home-title">Yum Union</h1>
        <h2 class="home-subtitle">Wasting None, Feeding Everyone!</h2>
      </div>
      <div class="second-container container">
          <div class="row ">
            <div class="col">
              <h3 class="home-info-title">Restaurants & Food Banks United</h3>
            </div>
            <div class="col">
              <p class="home-info-text">Yum Union bridges the gap between restaurants with surplus food and food banks seeking donations. Join this revolutionary platform to reduce waste and hunger together!</p>
            </div>
          </div>
      </div>
      <div class="third-container container">
        <div class="row row-cols-2 align-items-center">
          <div class="col-8 ">
            <h3 class="home-info-title">Ready to make a difference? Join Food Connect.</h3>
            <div class="home-auth col-4 mt-4 d-flex justify-content-between">
              <router-link v-if="loggedOut" to="/register" class="col btn btn-secondary button me-1">Register</router-link>
              <router-link v-if="loggedOut" to="/login" class="col btn btn-secondary button ms-1" style="background-color: #5465FF;">Login</router-link>
              <button v-else class="col btn btn-secondary button ms-1" style="background-color: #5465FF;">Already Logged In</button>
            </div>
          </div>
          <div class="col-4">
              <img src="../../public/images/home-door.png" alt="Image" class="door">
          </div>
        </div>
      </div>
      <div class="fourth-container container">
        <div class="row row-cols-2 align-items-center">
          <div class="col-7">
            <h3 class="home-info-title-sm mb-5">Intuitive Dashboard for Food Surplus Management </h3>
            <p class="home-info-text">As a <strong>restaurant</strong>, easily manage surplus food ensuring your restaurant’s excess is put to use for the betterment of the local community. As a <strong>food bank</strong> browse and request food donations. </p>
          </div>
          <div class="col-5">
            <img src="../../public/images/home-dashboard.png" alt="Image" class="home-img">
          </div>
        </div>
      </div>

        <div class="fifth-container container">
          <div class="row">
            <div class="col-12 text-left mb-5">
              <h3 class="home-info-title">Frequently Asked Questions</h3>
            </div>
          </div>
          <div class="row">
              <div class="col-md-4">
                  <div class="row-6 home-info-text"><strong>How Can I Join</strong></div>
                  <div class="row-6 home-info-text"><p>Simply click the “Sign Up” button and provide the details of your restaurant or food bank.</p></div>
              </div>
              <div class="col-md-4">
                  <div class="row-6 home-info-text"><strong>Is it free?</strong></div>
                  <div class="row-6 home-info-text"><p>Absolutely! Food Connect is free for both restaurants and food banks.</p></div>
              </div>
              <div class="col-md-4">
                  <div class="row-6 home-info-text"><strong>How Can I Contribute</strong></div>
                  <div class="row-6 home-info-text"><p>We are an open source project. You can help out through our <a href="https://github.com/youngwonks-coding-school/ywsos2023" target="_blank"><i class="fab fa-github"></i> GitHub</a> </p></div>
              </div>
            </div>
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