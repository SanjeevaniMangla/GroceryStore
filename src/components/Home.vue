<template>
    <nav id="home-nav" class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div id="home-search-nav" class="navbar-nav">
            <a v-if="isAuthenticated" id="home-search-category" class="nav-item nav-link"><router-link to="/search/categories">Search Category</router-link></a>
            <a v-if="isAuthenticated" id="home-search-products" class="nav-item nav-link"><router-link to="/search/products">Search products</router-link></a>
        </div>
        <div class="collapse navbar-collapse justify-content-end" id="navbar">
            <div id="home-navbar-end" class="navbar-nav">
                <!-- <a class="nav-item nav-link"><router-link to="/feed">Feed</router-link></a> -->
                <template v-if="isAuthenticated">
                    <template v-if="isAdmin">
                        <a id="home-admin-summary" class="nav-item nav-link"><router-link to="/summary">Summary</router-link></a>
                        <a id="home-admin-dashboard" class="nav-item nav-link"><router-link to="/admin/dashboard">Dashboard</router-link></a>
                    </template>
                    <template v-else>
                        <a id="home-user-bookings" class="nav-item nav-link"><router-link to="/bookings">Bookings</router-link></a>
                        <a id="home-user-dashboard" class="nav-item nav-link"><router-link to="/user/dashboard">Dashboard</router-link></a>
                    </template>
                    <div class="nav-item nav-link"  @click="logout" >Logout</div>
                </template>
                <template v-else>
                    <template v-if="isLoginPage">
                        <a id="home-sign-up" class="nav-item nav-link"><router-link to="/signup">Sign Up</router-link></a>
                    </template>
                    <template v-else-if="isSignUpPage">
                        <a id="home-login" class="nav-item nav-link"><router-link to="/login">Login</router-link></a>
                    </template>
                    <template v-else>
                        <a id="home-login" class="nav-item nav-link"><router-link to="/login">Login</router-link></a>
                        <a id="home-sign-up" class="nav-item nav-link"><router-link to="/signup">Sign Up</router-link></a>
                    </template>
                </template>
            </div>
        </div> 
        <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
        :message="$store.state.notification.message" @clear-notification="clearNotification"/>
    </nav>
</template>

<script>
import Notification from './Notification.vue'
export default{
    name : 'Home',
    components:{
        Notification
    },
    data(){
        return {
            notification: null
            
        };
    },
    computed:{
        isAuthenticated(){
            //Get the authenticationstatus from Vuex store
            return this.$store.state.isAuthenticated;
        },
        isLoginPage(){
            // Check if the current route is the login page
            return this.$route.path === '/login';
        },
        isSignUpPage(){
            // Check if the current route is the sign up page
            return this.$route.path === '/signup';
        },
        isAdmin() {
            const role = this.$store.state.userRole;
            if (role === 'Admin') {
                return true;
            }
            return false;
        }
    },
    methods:{
        clearNotification() {
            this.$store.commit('clearNotification');
        },
        handleDashboardClick() {
            const expiryTime = this.$store.state.expiryTime
            if (this.isAuthenticated && this.isTokenExpired(expiryTime)) {
                // Token has expired, perform logout
                this.logout()
            }
            else{
            const role = this.$store.state.userRole;
            if (role === 'Admin') {
                return this.$router.push('/admin/dashboard');
            }
            else if(role === 'User'){
                return this.$router.push('/user/dashboard');
            }
            else{
                return this.$router.push('/');
            }
            }
        },
        isTokenExpired(expiryTime) {
            if (expiryTime) {
                return  Date.now() > new Date(expiryTime) // 2 minutes in milliseconds
            }
            return false
        },
        async logout()
        {
            this.logoutInProgress = true;
            const response = await fetch("http://127.0.0.1:5000/logout", {
                method: "POST",
                headers : {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token')
                }
            }).then(async result => {
                const data = await result.json();
                this.$store.commit('setAuthentication', { isAuthenticated: false });
                this.$store.commit('setToken', { access_token: null });
                this.$store.commit('setExpiryTime', { expiryTime: null });
                this.$store.commit('setRole', { userRole: null });
                
                if (result.status === 200) {
                    this.$store.commit('setNotification', { variant: 'success', message: data.message });
                } else{
                    this.$store.commit('setNotification', { variant: 'error', message: 'Your session is expired. Login again!!' });
                }

                await new Promise(resolve => setTimeout(resolve, 1000)); // Delay for 1 second (adjust as needed)

                window.location.href = '/'
            })
        }
    }
}

</script>


<style scoped>

#home-nav{
    height: 60px;
}
a {
  text-decoration: none;
  color: white;
}

a:hover {
    color: rgb(255, 68, 0);
}

.login-link:hover,
.signup-link:hover {
  text-decoration: none;
}


</style>