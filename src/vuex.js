import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
      isAuthenticated: false,
      access_token: localStorage.getItem('access_token') || null,
      expiryTime: localStorage.getItem('expiryTine'),
      notification: null,
      userRole: null
    },
    mutations: {
      setAuthentication(state, payload) {
        state.isAuthenticated = payload.isAuthenticated;
      },
      setToken(state, payload) {
        state.access_token = payload.access_token;
        localStorage.setItem('access_token', payload.access_token);
      },
      setExpiryTime(state, payload){
        state.expiryTime = payload.expiryTime;
        localStorage.setItem('expiryTime', payload.expiryTime);
      },
      setNotification(state, { variant, message }) {
        state.notification = { variant, message };
      },
      clearNotification(state) {
        state.notification = null;
      },
      setRole(state, payload){
        state.userRole = payload.userRole;
        localStorage.setItem('selectedRole', payload.userRole);
      },
      setUserId(state, payload) { // Add the setUserId mutation
        state.userId = parseInt(payload.userId);
        localStorage.setItem('userId', parseInt(payload.userId));
      }
    }
  });
  

  export default store;