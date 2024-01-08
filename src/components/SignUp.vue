<template>
    <div>
        <Home />
        <div id="sign-up">
            <h2 id="sign-up-input" class="input">Sign Up</h2>
            <div id="sign-up-form" class="form-group">
                <div id="sign-up-error-message" v-if="errorMessages.length > 0 || serverErrorMessages.length > 0" class="error-message">
                    <ul>
                        <template v-if="errorMessages.length > 0">
                            <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                        </template>
                        <template v-else-if="serverErrorMessages.length > 0">
                            <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                        </template>
                    </ul>
                </div>
                <label for="email" :style="{ marginTop: errorMessageMarginTop }" class="text-left signup-form-label">Email Address</label>
                <input type="text" v-model="email"  class="form-control" placeholder="Enter Email" size="10"/>
                
                <label for="username" :style="{ marginTop: errorMessageMarginTop }" class="text-left signup-form-label">Username</label>
                <input type="text" v-model="username"  class="form-control" placeholder="Enter Username" size="10"/>
                
                <label for="password" :style="{ marginTop: errorMessageMarginTop }" class="signup-form-label">Password</label>
                <input type="password" v-model="password" class = "form-control" placeholder="Enter Password" size="15"/>
                
                <label for="confirm_password" :style="{ marginTop: errorMessageMarginTop }" class="signup-form-label" >Confirm Password</label>
                <input type="password" v-model="confirm_password"  class="form-control" placeholder="Enter Password Again" size="10"/>
                
                <div :style="{ marginTop: errorMessageMarginTop }" id="sign-up-dropdown" class="dropdown text-center">
                    <button class="btn btn-secondary dropdown-toggle" type="button" id="sign-up-dropdown-button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {{ selectedRole || 'Role' }}
                    </button>
                    <div id="sign-up-dropdown-values" class="dropdown-menu" aria-labelledby="sign-up-dropdown-button">
                        <a class="dropdown-item" v-for="role in roles" :key="role.id" @click="selectRole(role)">{{ role.storedName }}</a>
                    </div>
                </div>
                <br/>
                <div class="text-center">
                <button class="btn btn-primary" v-on:click="signup">Sign-up</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import Home from './Home.vue'
export default{
    name : 'SignUp',
    components : {
        Home
    },
    data(){
        return {
            email : "",
            username : "",
            password : "",
            confirm_password : "",
            errorMessages : [],
            roles: [],
            selectedRole: "",
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

        username(value) {
            this.handleInputChange('username', value);
            this.serverErrorMessages = []
        },

        password(value) {
            this.handleInputChange('password', value);
            this.serverErrorMessages = []
        },

        confirm_password(value) {
            this.handleInputChange('confirm_password', value);
            this.serverErrorMessages = []
        },
        selectedRole(value){
            this.handleInputChange('selectedRole', value);
            this.serverErrorMessages = []
        }
    },
    computed: {
        errorMessageMarginTop() {
            let messageLength = this.errorMessages.length > 0 ? this.errorMessages.length : this.serverErrorMessages.length;

            if(10 - (messageLength) * 2 >= 2)
                return `${10 - (messageLength) * 2}px`;
            else
                return `${2}px`;
        }
    },
    methods:{
        handleInputChange(fieldName, fieldValue){

            let message = '';
            if(fieldName === 'email'){
                message = 'Email should not be empty';
                this.validateEachEntity(this.email, message);
            }
            else if(fieldName === 'username'){
                message = 'Username should not be empty';
                this.validateEachEntity(this.username, message);
            }
            else if(fieldName === 'password'){
                message = 'Password should not be empty';
                this.validateEachEntity(this.password, message);
            }
            else if(fieldName === 'confirm_password'){
                message = 'Confirm password should not be empty';
                this.validateEachEntity(this.confirm_password, message);

                message = 'Password and confirm password do not match.';
                if(this.errorMessages.includes(message)){
                    let indexOFMessage = this.errorMessages.indexOf(message);
                    this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
                    if (this.password !== this.confirm_password){
                        this.errorMessages.splice(indexOFMessage, 0, message);
                    }
                }
                else{
                    if (this.password !== this.confirm_password){
                        this.errorMessages.push(message);
                    }
                }
            }
            else if(fieldName === 'selectedRole'){
                message = 'Role should be selected';
                this.validateEachEntity(this.selectedRole, message);
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

            message = 'Username should not be empty';
            this.validateEachEntity(this.username, message);
            
            message = 'Password should not be empty';
            this.validateEachEntity(this.password, message);
               
            message = 'Confirm password should not be empty';
            this.validateEachEntity(this.confirm_password, message);

            message = 'Role should be selected';
            this.validateEachEntity(this.selectedRole, message);
            
            if (this.password !== this.confirm_password) {
                this.errorMessages.push('Password and confirm password do not match.');
            }
        },
        async signup()
        {
            this.validation();
            if(this.errorMessages.length > 0){
                return;
            }

            const response = await fetch('http://127.0.0.1:5000/signup', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                input_email: this.email,
                input_username: this.username,
                input_password: this.password,
                input_confirm_password : this.confirm_password,
                input_role : this.selectedRole
                }),
            });

            const data = await response.json();

            if (response.ok) {
                // User is authenticated, redirect to home page
             this.$router.push('/login');
            } 
            else {
                // Show error message
                this.serverErrorMessages = data.error_messages;
            }   
        }
    }
}
</script>

 
  
<style scoped>
/* Container styles */
#sign-up-input {
    margin-top: 0px;
    text-align: center;
}

#sign-up-form {
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

#sign-up-error-message {
  width: 370px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#sign-up-error-message ul {
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


.signup-form-label{
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