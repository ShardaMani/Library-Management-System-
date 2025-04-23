import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    authToken: localStorage.getItem('authToken') || null,
    userRole: localStorage.getItem('userRole') || null, // Get userRole as a string directly
  },
  mutations: {
    setAuthToken(state, token) {
      state.authToken = token;
      localStorage.setItem('authToken', token);
    },
    setUserRole(state, role) {
      state.userRole = role;
      localStorage.setItem('userRole', role); // Store userRole as a string directly
    },
    clearAuth(state) {
      state.authToken = null;
      state.userRole = null;
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
    },
  },
  actions: {
    login({ commit }, credentials) {
      return axios.post('http://127.0.0.1:5000/login', credentials)
        .then(response => {
          const { token, role } = response.data;
          commit('setAuthToken', token);
          commit('setUserRole', role); // role should be a string (e.g., "user" or "librarian")
          return { token, role };
        });
    },
    logout({ commit }) {
      commit('clearAuth');
      // You can add additional logout logic here if needed
    },
  },
  getters: {
    isAuthenticated: state => !!state.authToken,
    userRole: state => state.userRole,
  },
});
