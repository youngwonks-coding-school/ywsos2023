<template>
  <nav :key="isLoggedIn" class="navbar navbar-expand-md d-flex justify-content-center navbar-floating" :class="{ 'dark-theme': isDarkTheme }">
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
          <div class="d-flex" v-else>
            <li class="nav-item">
            <a class="nav-link" href="/logout" @click="logout">Logout</a>
            </li>
            <li>
              <a class="nav-link" href="/dashboard" >Dashboard</a>
            </li>
            <li>
              <a class="nav-link" href="/profile" >Profile</a>
            </li>
          </div>
           <li class="nav-item">
            <a class="nav-link" href="/posts">Posts</a>
           </li>
          <li class="nav-item">
            <a class="nav-link" href="/maps">Maps</a>
          </li>
           <li class="nav-item">
            <div class="dropdown" href="/clock">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <span id="timezone">{{ currentTime }}</span>
              </a>
              <ul class="dropdown-menu" aria-labelledby="timezone">
                <li v-for="timezone in timezones" :key="timezone.identifier">
                  <a class="dropdown-item" href="#" @click="changeTimezone(timezone)">{{ timezone.label }}</a>
                </li>
              </ul>
            </div>
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
import { DateTime, IANAZone } from 'luxon';

export default {
  computed: {
    isLoggedIn() {
      return this.accessToken !== '';
    },
  },
  data() {
    return {
      accessToken: localStorage.getItem('accessToken') || '',
      isDarkTheme: true,
      currentTime: '',
      selectedTimezone: 'PST', // Default timezone
      timezones: [
        { identifier: 'Pacific/Pago_Pago', label: 'International Date Line West' },
        { identifier: 'SST', label: 'Samoa Standard Time' },
        { identifier: 'HST', label: 'Hawaii Standard Time' },
        { identifier: 'America/Anchorage', label: 'Alaska Standard Time' },
        { identifier: 'PST', label: 'Pacific Standard Time' },
        { identifier: 'MST7MDT', label: 'Mountain Standard Time' },
        { identifier: 'CST6CDT', label: 'Central Standard Time' },
        { identifier: 'EST5EDT', label: 'Eastern Standard Time' },
        { identifier: 'ART', label: 'Argentina Time' },
        { identifier: 'UTC-3', label: 'Brasília Time' },
        { identifier: 'UTC-1', label: 'Cape Verde Time' },
        { identifier: 'GMT', label: 'Greenwich Mean Time' },
        { identifier: 'UTC+1', label: 'British Summer Time' },
        { identifier: 'UTC+2', label: 'Central European Summer Time' },
        { identifier: 'UTC+3', label: 'Moscow Standard Time' },
        { identifier: 'UTC+4', label: 'Gulf Standard Time' },
        { identifier: 'IST', label: 'Indian Standard Time' },
        { identifier: 'UTC+7', label: 'Western Indonesian Time' },
        { identifier: 'JST', label: 'Japan Standard Time' },
        { identifier: 'UTC+10', label: 'Australian Eastern Standard Time' },
        { identifier: 'UTC+11', label: 'New Caledonia Time' },
        { identifier: 'UTC+12', label: 'New Zealand Standard Time' },
        { identifier: 'UTC+13', label: 'Tonga Time' },
        { identifier: 'UTC+10', label: 'Chamorro Standard Time' },
      ],
    };
  },
  
  mounted() {
    this.updateTime();
    setInterval(this.updateTime, 1000); 

      window.addEventListener('access-token-localstorage-changed', (event) => {
      this.accessToken = event.detail.storage;
    });
  },
  
  methods: {
    logout() {
      this.axiosInstance.get('/api/auth/logout', {
      headers: {Authorization: `Bearer ${localStorage.getItem('accessToken')}`}}).catch((error) => {console.log(error, "logging out");
      });

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
    
    updateTime() {
      let currentTime = DateTime.now().setZone(this.selectedTimezone);
      this.currentTime = currentTime.toFormat('hh:mm:ss a');
    },
    changeTimezone(timezone) {
      this.selectedTimezone = timezone.identifier;
      this.updateTime();
    },
  },
};
</script>
