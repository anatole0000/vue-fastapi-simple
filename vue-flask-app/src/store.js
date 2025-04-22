// store/index.js

import { createStore } from 'vuex';

export default createStore({
  state: {
    accessToken: null,  // Store the JWT token
  },
  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token;
    },
  },
  actions: {
    login({ commit }, token) {
      commit('setAccessToken', token);
    },
    logout({ commit }) {
      commit('setAccessToken', null);
    },
  },
  getters: {
    getAccessToken(state) {
      return state.accessToken;
    },
  },
});
