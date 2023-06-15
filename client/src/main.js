import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";
import "bootstrap";
import "../scss/custom.scss";
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

import axios from 'axios';
axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL


const app = createApp(App);

app.use(router);
app.use(ToastPlugin, {
    // One of the options
    position: 'top-right'
});

app.mount("#app");
