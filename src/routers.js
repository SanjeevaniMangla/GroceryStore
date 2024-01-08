import SignUp from './components/SignUp.vue'
import Home from './components/Home.vue'
import Login from './components/Login.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import ManagerDashboard from './components/ManagerDashboard.vue'
import UserDashboard from './components/UserDashboard.vue'
import SearchCategory from './components/SearchCategory.vue'
import SearchProduct from './components/SearchProduct.vue'
import Bookings from './components/Bookings.vue'
import Summary from './components/Summary.vue'
import store from './vuex';
import VueRouter from 'vue-router'

const routes = [
    {
        name : 'SignUp',
        component : SignUp,
        path : '/signup',
        meta: { 
            requiresGuest: true 
        }
    },
    {
        name : 'Home',
        component : Home,
        path : '/'
    },
    {
        name : 'Login',
        component : Login,
        path : '/login',
        meta: { 
            requiresGuest: true 
        }
    },
    {
        name : 'AdminDashboard',
        component : AdminDashboard,
        path : '/admin/dashboard',
        meta: {
            requiresAuth: true,
            requiresRole: 'Admin'
        }
    },
    {
      name : 'UserDashboard',
      component : UserDashboard,
      path : '/user/dashboard',
      meta: {
        requiresAuth: true,
        requiresRole: 'User'
      }
    },
    {
      name : 'SearchCategory',
      component : SearchCategory,
      path : '/search/categories',
      meta: {
        requiresAuth: true
      }
    },
    {
      name : 'SearchProduct',
      component : SearchProduct,
      path : '/search/products',
      meta: {
        requiresAuth: true
      }
    },
    {
      name : 'Bookings',
      component : Bookings,
      path : '/bookings',
      meta: {
        requiresAuth: true,
        requiresRole: 'User'
      }
    },
    {
      name : 'Summary',
      component : Summary,
      path : '/summary',
      meta : {
        requiresAuth : true,
        requiresRole : 'Admin'
      }
    },
    {
      name : 'ManagerDashboard',
      component : ManagerDashboard,
      path : '/manager/dashboard',
      meta: {
          requiresAuth: true,
          requiresRole: 'Manager'
      }
  }
];

const router = new VueRouter({
    routes
})


router.beforeEach(async (to, from, next) => {
    const isAuthenticated = store.state.isAuthenticated;
    const requiresAuth = to.meta.requiresAuth;
    const requiresGuest = to.meta.requiresGuest;
    const role = store.state.userRole;
    const requiredRole = to.meta.requiresRole;

    if ((requiresAuth && !isAuthenticated) || (requiresGuest && isAuthenticated)) {
      next('/');
    } else {
      const accessToken = store.state.access_token;
      const expiryTime = store.state.expiryTime;
  
      if (requiresAuth && accessToken && expiryTime) {
        
          store.commit('setAuthentication', { isAuthenticated: true });
          store.commit('setToken', { access_token: accessToken });
          store.commit('setExpiryTime', { expiryTime : expiryTime })

          if(requiredRole)
          {
            if(role !== requiredRole){
              // Show popup or notification indicating unauthorized access
              store.commit('setNotification', {
                variant: 'error',
                message: 'You are not authorized to access this page.'
              });
              setTimeout(() => {
                store.commit('clearNotification');
              }, 3000);
              next('/');
            }
            else{
              next();
            }
          }
          else{
            next();
          }
        } else {
        next();
      }
    }
  });

export default router;