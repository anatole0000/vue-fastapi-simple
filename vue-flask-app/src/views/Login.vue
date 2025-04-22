<template>
    <div class="container">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserLogin',
    data() {
      return {
        username: '',
        password: '',
        message: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/login', {
            username: this.username,
            password: this.password
          });
          
          // Handle success response
          if (response.data && response.data.access_token) {
            // Store the token in Vuex store or localStorage
            this.$store.dispatch('login', response.data.access_token);  // Vuex store dispatch
            this.$router.push('/');  // Redirect to profile page after successful login
          } else {
            this.message = 'Login failed. Please try again.';
          }
        } catch (error) {
          // Handle Axios error with detailed checks
          if (error.response) {
            // Error from server (e.g., invalid username or password)
            this.message = error.response.data.msg || 'Login failed. Please try again.';
          } else if (error.request) {
            // No response received from server (e.g., network issues)
            this.message = 'Network error: Server not reachable.';
          } else {
            // Other errors (e.g., bad request formatting)
            this.message = `Error: ${error.message}`;
          }
        }
      }
    }
  };
  </script>
  