// main.js
import { createApp } from 'vue';
import App from './App.vue';
import store from './store';  // Vuex store
import router from './router';  // Import router

const app = createApp(App);
app.use(store);
app.use(router);  // Register router
app.mount('#app');
