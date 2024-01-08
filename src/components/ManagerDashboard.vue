<template>
    <div>
      <Home/>
      <div class="category-circle-container">
        <div class="category-circle" @click="openModal">
          <div class="category-plus-container">
            <div class="category-horizontal-plus"></div>
            <div class="category-vertical-plus"></div>
          </div>
        </div>
      </div>
  
      <b-modal id="circle-modal" v-model="showModal" size="lg" variant="primary" no-close-on-backdrop>
        <template #modal-header>
          <h3 class="mb-0">Add Category</h3>
        </template>
        <template #default>
          <div class="form-group">
            <div id="category-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isSubmitButtonClicked" class="category-error-message">
                <ul>
                    <template v-if="errorMessages.length > 0">
                      <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                    </template>
                    <template v-else-if="serverErrorMessages.length > 0">
                      <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                    </template>
                </ul>
            </div>
          </div>
          <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="input_name" class="form-control" v-model="name" />
          </div>
          <div class="form-group">
            <label for="image">Image:</label>
            <input type="file" id="image" class="form-control-file" @change="handleImageUpload" />
          </div>
        </template>
        <template #modal-footer>
          <b-btn class="primary" @click="submitForm">Submit</b-btn>
          <b-btn @click="closeModal">Close</b-btn>
        </template>
      </b-modal>
      <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
          :message="$store.state.notification.message" @clear-notification="clearNotification"/>
  
  
      <div>
        <div class="row mb-4" v-for="(row, index) in rows" :key="index">
          <div class="col-4" v-for="category in row" :key="category.id">
            <b-card :header="category.name" header-tag="header" bg-variant="secondary" text-variant="white">
              <b-card-text>
                <ManagerProduct :category="category" />
                <ManagerCategory :category="category" @category-deleted="removeCategory"/>
              </b-card-text>
              <template #footer>
                <small class="text-muted">Last updated 3 mins ago</small>
              </template>
            </b-card>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Home from './Home.vue'
  import ManagerProduct from './ManagerProduct.vue'
  import ManagerCategory from './ManagerCategory.vue'
  import Notification from './Notification.vue'
  export default {
    name: 'ManagerDashboard',
    components: {
      Home, ManagerProduct,ManagerCategory,Notification
    },
    data() {
      return {
        showModal: false,
        name: "",
        image: "",
        errorMessages: [],
        serverErrorMessages: [],
        isSubmitButtonClicked: false,
        notification: null,
        categories: [],
        cardsPerRow: 3
      }
    },
    mounted() {
      this.fetchCategories();
      document.addEventListener('click', this.redirectIfTokenExpired);
    },
    beforeUnmount() {
      document.removeEventListener('click', this.redirectIfTokenExpired);
    },
    computed: {
      rows() {
        // Slice the categories array into chunks based on cardsPerRow
        return this.chunkArray(this.categories, this.cardsPerRow);
      }
    },
    watch: {
  
      name(value) {
        this.handleInputChange('Name', value);
        this.serverErrorMessages = []
  
      },
  
    },
    methods: {
      clearNotification() {
              this.$store.commit('clearNotification');
          },
          removeCategory(categoryId) {
        this.categories = this.categories.filter(category => category.id !== categoryId);
      },
      getColClass(categoriesCount) {
        const colSize = Math.floor(12 / categoriesCount);
        return `col-${colSize}`;
      },
      chunkArray(array, size) {
        const result = [];
        for (let i = 0; i < array.length; i += size) {
          result.push(array.slice(i, i + size));
        }
        return result;
      },
      isTokenExpired(expiryTime, isAuthenticated) {
        if (isAuthenticated) {
          if (expiryTime) {
            return Date.now() > new Date(expiryTime);
          } else {
            return true;
          }
        }
        return false;
      },
      redirectIfTokenExpired() {
        const expiryTime = this.$store.state.expiryTime;
        const isAuthenticated = this.$store.state.isAuthenticated;
        if (this.isTokenExpired(expiryTime, isAuthenticated)) {
          // Token has expired, redirect to home page
          this.$store.commit('setAuthentication', {
            isAuthenticated: false
          });
          this.$store.commit('setToken', {
            access_token: null
          });
          this.$store.commit('setExpiryTime', {
            expiryTime: null
          });
          this.$store.commit('setNotification', {
            variant: 'error',
            message: 'Your session is expired. Login again!!'
          });
          this.$router.push('/');
        }
      },
      handleInputChange(fieldName, fieldValue) {
        let message = '';
        message = fieldName + ' cannot be empty';
        this.validateEachEntity(fieldValue, message);
      },
      openModal() {
        this.showModal = true;
      },
      closeModal() {
        this.errorMessages = [];
        this.serverErrorMessages = [];
        this.showModal = false;
        this.isSubmitButtonClicked = false;
      },
      handleImageUpload(event) {
        // Handle the image upload here
        this.image = event.target.files[0];
      },
      validateEachEntity(entityToValidate, message) {
        if (this.errorMessages.includes(message)) {
          let indexOFMessage = this.errorMessages.indexOf(message);
          this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
          if (entityToValidate == null || entityToValidate == '') {
            this.errorMessages.splice(indexOFMessage, 0, message);
          }
        }
        else {
          if (entityToValidate == null || entityToValidate == '') {
            this.errorMessages.push(message);
          }
        }
      },
      validation() {
  
        let message = 'Name cannot be empty'
        this.validateEachEntity(this.name, message);
  
        message = 'Image cannot be empty';
        this.validateEachEntity(this.image, message);
  
        message = 'Invalid image file format. Please select a valid image file';
        const allowedExtensions = ["jpg", "jpeg", "png", "gif"];
        const fileExtension = this.image.name.split(".").pop().toLowerCase();
        if (this.errorMessages.includes(message)) {
          if (allowedExtensions.includes(fileExtension)) {
            this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
          }
        }
        else {
          if (!allowedExtensions.includes(fileExtension)) {
            this.errorMessages.push(message);
          }
        }
      },
      async submitForm() {
        this.isSubmitButtonClicked = true;
        this.validation();
        if (this.errorMessages.length > 0) {
          return;
        }
  
        // Create a FormData object
        const formData = new FormData();
        formData.append('input_name', this.name);
        formData.append('input_image', this.image);
        const user_id = parseInt(localStorage.getItem('userId'));
  
        const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category_manager_api`, {
          method: "POST",
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
          body: formData,
        }).then(async result => {
          const data = await result.json();
          if (result.ok) {
            this.$store.commit('setNotification', { variant: 'success', message: data.message });
            this.fetchCategories();
          }
          else {
            this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
          }
          this.closeModal();
        })
      },
      async fetchCategories() {
  
        const user_id = parseInt(localStorage.getItem('userId'));
        const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category_manager_api`, {
          method: "GET",
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          }
        }).then(async result => {
          const data = await result.json();
          if (result.ok) {
            this.categories = data.categories
          }
          else if (result.status === 409) {
  
          }
          else {
            if(!data.error_messages.includes("There are no categories"))
              this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
          }
        })
      }
    }
  }
  </script>
  
  <style scoped>
  .category-circle-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 80px);
  }
  
  .category-circle {
    position: relative;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background-color: rgb(44, 108, 128);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  
  .category-plus-container{
    position: relative;
    width: 60%;
    height: 60%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .category-horizontal-plus,
  .category-vertical-plus {
    position: absolute;
    background-color: #FFFFFF;
  }
  
  .category-horizontal-plus {
    width: 50%;
    height: 2px;
    top: 50%;
    transform: translateY(-50%);
  }
  
  .category-vertical-plus {
    width: 2px;
    height: 50%;
    left: 50%;
    transform: translateX(-50%);
  }
  #category-error-message {
    width: 750px;
    margin-top: -15px;
    border-color: black; 
    border: 2px solid black;
  }
  
  #category-error-message ul {
    color: white;
    background-color: lightcoral;
    padding: 10px;
    margin: 0;
    list-style-type: none;
  }
  
  
  </style>
  
    