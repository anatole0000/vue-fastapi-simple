import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Profile from '../views/Profile.vue';
import ItemList from '../components/ItemList.vue';

const routes = [
  { path: '/', name: 'Home', component: ItemList },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Add route guard to check for authentication
router.beforeEach((to, from, next) => {
  // Assuming you store the user's auth status in localStorage or Vuex
  const isAuthenticated = localStorage.getItem('token'); // Replace with your auth logic

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to login page if trying to access a protected route
    next({ path: '/login' });
  } else {
    // Allow navigation if authenticated or not a protected route
    next();
  }
});

export default router;
