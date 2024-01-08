import Vue from 'vue'
import App from './App.vue'
import router from './routers'
import store from './vuex'
import { BootstrapVue } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueRouter from 'vue-router'

Vue.use(BootstrapVue);
Vue.use(VueRouter);


// Check for the token and expiry time in local storage
const access_token = localStorage.getItem('access_token');
const expiryTime = localStorage.getItem('expiryTime');
const selectedRole = localStorage.getItem('selectedRole');

if (access_token && expiryTime && Date.now() > new Date(expiryTime)) {
  // Token has expired, perform logout
  localStorage.removeItem('access_token');
  localStorage.removeItem('expiryTime');
  store.commit('setAuthentication', { isAuthenticated: false });
  store.commit('setToken', { access_token: null });
} else if (access_token && expiryTime && Date.now() < new Date(expiryTime)) {
  // If the token exists and is not expired, update the Vuex store with the authentication status
  store.commit('setAuthentication', { isAuthenticated: true });
  store.commit('setToken', { access_token });
  store.commit('setExpiryTime', { expiryTime });
  store.commit('setRole', { userRole: selectedRole });
}
else{
  store.commit('setAuthentication', { isAuthenticated: false});
  store.commit('setToken', {access_token: null});
}


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
