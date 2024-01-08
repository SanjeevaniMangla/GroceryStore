<template>
    <div>
        <Home />
        <h2 id="login-input" class="input text-center">Login</h2>
        <div id="login-form" class="form-group">
            <div id="login-error-message" v-if="errorMessages.length > 0 || serverErrorMessages.length > 0" class="error-message">
                <ul>
                    <template v-if="errorMessages.length > 0">
                        <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                    </template>
                    <template v-else-if="serverErrorMessages.length > 0">
                         <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                    </template>
                </ul>
            </div>

            <label for="email" :style="{ marginTop: errorMessageMarginTop }" class="text-left login-form-label">Email Address</label>
            <input type="text" v-model="email" id="email_id" name="email" class="form-control" placeholder="Enter Email" size="10" />
            
            <label for="password" :style="{ marginTop: errorMessageMarginTop }" class="text-left login-form-label">Password</label>
            <input type="password" v-model="password" id="password_id" name="password" class="form-control" placeholder="Enter Password"
                size="15" />

            <div id="login-dropdown" :style="{ marginTop: errorMessageMarginTop }" class="dropdown text-center">
                <b-dropdown v-model="selectedRole" id="login-dropdown-button" :text="selectedRole || 'Role'">
                    <b-dropdown-item v-for="role in roles" :key="role.id" :value="role.storedName" @click="selectRole(role)">
                        {{ role.storedName }}
                    </b-dropdown-item>
                </b-dropdown>
            </div>

            <div class="text-center" style="padding-top: 20px;">
                <button class="btn btn-primary" v-on:click="login">Login</button>
            </div>
        </div>
    </div>
</template>


<script>
import Home from './Home.vue'
import { BDropdown, BDropdownItem } from 'bootstrap-vue';
export default{
    name : 'Login',
    components : {
        Home,
        BDropdown,
        BDropdownItem,
    },
    data(){
        return {
            email : "",
            password : "",
            errorMessages: [],
            selectedRole: "",
            roles: [],
            serverErrorMessages: []
        };
    },
    mounted(){
        this.fetchRoles();
    },
    watch: {
        email(value) {
            this.handleInputChange('email', value);
            this.serverErrorMessages = []
        },

        password(value) {
            this.handleInputChange('password', value);
            this.serverErrorMessages = []

        },

        selectedRole(value){
            this.handleInputChange('selectedRole', value);
            this.serverErrorMessages = []

        }
    },
    computed: {
        errorMessageMarginTop() {
            let len = this.errorMessages.length > 0 ? this.errorMessages.length : this.serverErrorMessages.length;
            if(20 - (len) * 2 >= 2)
                return `${20 - (len) * 2}px`;
            else
                return `${2}px`;
        }
    },
    methods:{
        handleInputChange(fieldName, fieldValue){

            let message = '';
            if(fieldName === 'email'){
                message = 'Email should not be empty';
                this.validateEachEntity(fieldValue, message);
            }
            else if(fieldName === 'password'){
                message = 'Password should not be empty';
                this.validateEachEntity(fieldValue, message);
            }
            else if(fieldName === 'selectedRole'){
                message = 'Role should be selected';
                this.validateEachEntity(fieldValue, message);
            }
        },
        async fetchRoles(){
            try{
                const response = await fetch('http://127.0.0.1:5000/api/roles');
                const data = await response.json();
                this.roles = data;
            }
            catch(error){
                this.errorMessages.push("Error fetching roles");
            }
        },
        selectRole(role){
            this.selectedRole = role.storedName;
        },
        validateEachEntity(entityToValidate, message){
            if(this.errorMessages.includes(message)){
                let indexOFMessage = this.errorMessages.indexOf(message);
                this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
                if(entityToValidate == null || entityToValidate == ''){
                    this.errorMessages.splice(indexOFMessage, 0, message);
                }
            }
            else{
                if(entityToValidate == null || entityToValidate == ''){
                    this.errorMessages.push(message);
                }
            }
        }
        ,
        validation(){

            let message = 'Email should not be empty'
            this.validateEachEntity(this.email, message);

            message = 'Password should not be empty';
            this.validateEachEntity(this.password, message);

            message = 'Role should be selected';
            this.validateEachEntity(this.selectedRole, message);
        },
        async login()
        {
            this.validation();
            if(this.errorMessages.length > 0){
                return;
            }

            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    input_email : this.email,
                    input_password : this.password,
                    input_role: this.selectedRole
                }),
            }).then(async result => {
                const data = await result.json();
                if (result.status === 200) {
                    this.$store.commit('setAuthentication', { isAuthenticated: true });
                    this.$store.commit('setToken', { access_token: data.access_token });
                    this.$store.commit('setExpiryTime', { expiryTime: data.expires });
                    this.$store.commit('setRole', { userRole: this.selectedRole});
                    this.$store.commit('setUserId', { userId: data.id });
                    if(this.selectedRole === 'Admin'){
                        this.$router.push('/admin/dashboard');
                    }
                    else if(this.selectedRole === 'Manager'){
                        this.$router.push('/manager/dashboard');
                    }
                    else{
                        this.$router.push('/user/dashboard');
                    }
                } else{
                    this.serverErrorMessages = data.error_messages;
                }
                
            }

            )

            
        }
    }
}
</script>

<style scoped>
/* Container styles */
#login-input {
    margin-top: 120px;
    text-align: center;
}

#login-form {
    width: 400px;
    padding: 20px;
    margin: 0 auto;
    background-color: rgb(203, 235, 135);
    border: 8px double red;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}

#login-error-message {
  width: 370px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#login-error-message ul {
  color: white;
  background-color: lightcoral;
  padding: 10px;
  margin: 0;
  list-style-type: none;
}

/* Form field styles */
.form-control {
    width: 300px;
    height: 40px;
    border: 1px solid black;
    padding: 2px;
    margin-bottom: 10px;
    box-sizing: border-box;
}


.login-form-label{
    text-align: left;
}

/* Dropdown styles */

.dropdown-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 300px;
    height: 40px;
    border: 1px solid black;
    cursor: pointer;
}

.dropdown-menu {
    width: 300px;
}

.dropdown-item {
    padding: 10px;
    cursor: pointer;
}

/* Button styles */
.btn-primary {
    width: 150px;
    height: 40px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}

</style>