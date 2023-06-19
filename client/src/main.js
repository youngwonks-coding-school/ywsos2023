import "bootstrap";
import "../scss/custom.scss";
import 'vue-toast-notification/dist/theme-bootstrap.css';

import App from "./App.vue";
import ToastPlugin from 'vue-toast-notification';
import axios from 'axios';
import { createApp } from "vue";
import router from "./router";

(async () => {
    axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL;
    document.documentElement.setAttribute('data-theme', localStorage.getItem('theme') || 'light');
    // Wait for the baseURL to be set
    await new Promise(resolve => setTimeout(resolve, 1000));
  
    const app = createApp(App);
  
    app.use(router);
    app.use(ToastPlugin, {
      position: 'top-right'
    });
  
    app.mount("#app");
  })();