<template>
    <div class="container">
      <h1>Welcome to the Home Page</h1>
      <div v-if="isAuthenticated">
        <p>You are logged in!</p>
        <button @click="logout">Logout</button>
      </div>
      <div v-else>
        <p>Please log in to see the content.</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage',
    computed: {
      isAuthenticated() {
        return this.$store.getters.isAuthenticated;
      }
    },
    methods: {
      logout() {
        this.$store.dispatch('logout');
        this.$router.push('/login');  // Redirect to login after logout
      }
    }
  };
  </script>
  