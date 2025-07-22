import { createApp } from 'vue';
import App from './App.vue';
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; 
import { aliases, mdi } from 'vuetify/iconsets/mdi';
import router from './router'; 
import { createPinia } from 'pinia'
import axios from 'axios'
import './style.css';

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false, 
        colors: {
          primary: '#6200ee',
          secondary: '#03dac6',
          background: '#ffffff',
          surface: '#ffffff',
          error: '#b00020',
        },
      },
    },
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
});
axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App);


app.use(vuetify);
app.use(createPinia())
app.use(router, axios)
app.mount('#app');

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('user.access');
  // Only attach token to secure endpoints
  if (token && !config.url.includes('request-password-reset')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
