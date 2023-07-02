import "bootstrap";
import "../scss/custom.scss";
import 'vue-toast-notification/dist/theme-bootstrap.css';

import App from "./App.vue";
import ToastPlugin from 'vue-toast-notification';
import axios from 'axios';
import { createApp } from "vue"
;
import router from "./router";

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:4000/api', // Assuming the base URL is '/api'
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('accessToken');
    if (!config.skipAuth){
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.response.status === 401) {
      try {
        const refreshResponse = await axiosInstance.post('/auth/refresh', {
          Authorization: `Bearer ${localStorage.getItem('refreshToken')}`
        });
        localStorage.setItem('accessToken', refreshResponse.data.accessToken);
        return axiosInstance(error.response.config);
      } catch (error) {
        $toast.error('Axios Instance \n Refresh token error');
        console.log('Axios Instance \n Refresh token error:', error)
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

//If user is logged in get their business type and set to local storage
//This value is accessed in router/index.js to determine which profile view to render
//The value is initially set in the register view (tab selection)

if (localStorage.getItem('accessToken')) {
  console.log("attempting to access business type")
  axiosInstance.get('/api/auth/get-business-type', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`
    }
  }).then((response) => {
    console.log('getting business type: ', response.data.business_type)
    localStorage.setItem('business_type', response.data.business_type)
  }).catch((error) => {
    console.log('error', error)
  })
}



axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL;
document.documentElement.setAttribute('data-theme', localStorage.getItem('theme') || 'light');

// Wait for the baseURL to be set
await new Promise(resolve => setTimeout(resolve, 1000));

const app = createApp(App);

app.use(router);
app.use(ToastPlugin, {
  position: 'top-right'
});

app.config.globalProperties.axiosInstance = axiosInstance;

app.mount("#app");