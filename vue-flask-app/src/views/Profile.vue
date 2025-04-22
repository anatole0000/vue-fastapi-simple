<template>
    <div class="container">
      <h2>User Profile</h2>
      <div v-if="profile">
        <form @submit.prevent="updateProfile">
          <div>
            <label>Username</label>
            <input v-model="profile.username" disabled />
          </div>
          <div>
            <label>Email</label>
            <input v-model="profile.email" />
          </div>
          <div>
            <label>New Password</label>
            <input v-model="password" type="password" />
          </div>
          <button type="submit">Update</button>
          <p v-if="message">{{ message }}</p>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserProfile',
    data() {
      return {
        profile: null,
        password: '',
        message: ''
      };
    },
    created() {
      this.getProfile();
    },
    methods: {
      async getProfile() {
        try {
          const res = await axios.get('http://127.0.0.1:5000/profile', {
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`
            }
          });
          this.profile = res.data;
        } catch (err) {
          this.message = 'Failed to load profile.';
        }
      },
      async updateProfile() {
        try {
          const res = await axios.put('http://127.0.0.1:5000/profile', {
            email: this.profile.email,
            password: this.password || undefined
          }, {
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`
            }
          });
          this.message = res.data.msg;
          this.password = '';
        } catch (err) {
          this.message = 'Update failed.';
        }
      }
    }
  };
  </script>
  