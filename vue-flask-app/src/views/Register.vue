<template>
    <div class="container">
      <h1 class="text-center mt-5">Register</h1>
      <form @submit.prevent="handleRegister" class="w-50 mx-auto">
        <div class="form-group mb-3">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            class="form-control"
            placeholder="Enter your username"
            required
          />
        </div>
  
        <div class="form-group mb-3">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="form-control"
            placeholder="Enter your email"
            required
          />
        </div>
  
        <div class="form-group mb-3">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-control"
            placeholder="Enter your password"
            required
          />
        </div>
  
        <div class="form-group mb-3">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            class="form-control"
            placeholder="Confirm your password"
            required
          />
        </div>
  
        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>
  
      <p class="text-center mt-3">
        Already have an account? <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserRegister',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      };
    },
    methods: {
      async handleRegister() {
        // Simple validation for matching passwords
        if (this.password !== this.confirmPassword) {
          alert('Passwords do not match!');
          return;
        }
  
        // Add more client-side validation if necessary (e.g., valid email format)
  
        try {
          // Make the registration request to the backend API
          const response = await axios.post('http://127.0.0.1:5000/register', {
            username: this.username,
            email: this.email,
            password: this.password,
          });
  
          // Check if the response contains a success message and handle accordingly
          if (response.data.msg === 'User created successfully') {
            this.$router.push('/login'); // Redirect to login page after successful registration
          } else {
            alert('Registration failed: ' + response.data.msg);
          }
        } catch (error) {
          console.error('Error during registration:', error);
          alert('An error occurred during registration');
        }
      },
    },
  };
  </script>
  