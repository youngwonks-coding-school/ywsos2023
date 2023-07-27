import "bootstrap";
import "../scss/custom.scss";
import 'vue-toast-notification/dist/theme-bootstrap.css';

import {
  BiExclamationCircleFill,
  BiPencilSquare,
  BiTrash,
  IoAddCircleSharp,
  IoCloseOutline,
  RiSave3Line
} from "oh-vue-icons/icons";
import { OhVueIcon, addIcons } from "oh-vue-icons";

import App from "./App.vue";
import ToastPlugin from 'vue-toast-notification';
import axios from 'axios';
import { createApp } from "vue"
;
import router from "./router";
import VueGoogleMaps from '@fawmi/vue-google-maps';

addIcons(BiTrash, IoAddCircleSharp, IoCloseOutline, RiSave3Line, BiPencilSquare, BiExclamationCircleFill);

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_SERVER_URL, // Assuming the base URL is '/api'
});

// Request interceptor
axiosInstance.interceptors.request.use((config) => {
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
axiosInstance.interceptors.response.use((response) => {
    console.log("response", response)
    return response;
  },
  (error) => {
    if (error.response.status === 401) {
      try {
        console.log("refreshing")
        const refreshResponse = axios.post('api/auth/refresh', {
          Authorization: `Bearer ${localStorage.getItem('refreshToken')}`
        });
        console.log("refresh", refreshResponse.data.accessToken)
        localStorage.setItem('accessToken', refreshResponse.data.accessToken);
        return axiosInstance(error.response.config);
        
      } catch (error) {
        $toast.error('Axios Instance \n Refresh token error');
        console.log('Axios Instance \n Refresh token error:', error)
      }
  }
  });

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





(async () => {
  
  let myapiKey=null;
    try {
      axios.post("http://localhost:5000/api/maps/get_api_key")
        .then(response => {
          myapiKey = response.data.key;
          return { myapiKey }
        })
    } catch (error) {
      console.error('Failed to fetch API key:', error);
      return;
    }


    axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL;
    document.documentElement.setAttribute('data-theme', localStorage.getItem('theme') || 'light');
    // Wait for the baseURL to be set
    await new Promise(resolve => setTimeout(resolve, 1000));
  
    const app = createApp(App);

    app.config.globalProperties.axiosInstance = axiosInstance;
    app.component("v-icon", OhVueIcon);
  
    app.use(router);
    app.use(ToastPlugin, {
      position: 'top-right'
    });

      app.use(VueGoogleMaps, {
      load: {
        key: myapiKey
      }
    });
  
    app.mount("#app");
  })();

