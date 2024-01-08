<template>
    <div>
      <div id="products-box">
        <!-- Loop through each show in the theatre.shows array -->
        <div v-for="product in category.products" :key= "product.id" id="product-item">
          <!-- Show details -->
          <div id="product-details">
            <!-- Add your show details content here -->
            <!-- For example, you can display show name, date, etc. -->
            <div id="each-detail">
              <div id="product-name" class="right-details">
              Product Name: {{ product.name }}
              </div>
            </div>
            <div id="each-detail">
              <div id="product-price" class="left-details">
                Price: {{ product.price }}
              </div>
            </div>
          </div>
          <!-- Show Actions dropdown -->
          <div id="product-actions">
            <!-- Actions dropdown menu -->
            <b-dropdown  variant="info"  class="mr-2">
              <template #button-content>
                Actions
              </template>
              <b-dropdown-item @click="editProduct(product)">Edit Product</b-dropdown-item>
              <b-dropdown-item @click="deleteProduct(category, product)">Delete Product</b-dropdown-item>
            </b-dropdown>
          </div>
          <b-modal id="admin-edit-product-modal" v-model="showEditProductModal" size="lg" variant="primary" no-close-on-backdrop>
            <template #modal-header>
              <h3 class="mb-0">Edit Product</h3>
            </template>
            <template #default>
              <div class="form-group">
                <div id="admin-product-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isEditSubmitButtonClicked" class="admin-product-error-message">
                    <ul>
                        <template v-if="errorMessages.length > 0">
                          <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                        </template>
                        <template v-else-if="serverErrorMessages.length > 0">
                          <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                        </template>
                    </ul>
                </div>
                <label for="name">Name:</label>
                <input type="text" id="name" class="form-control" v-model="editProductData.name" />
              </div>
              <div class="form-group">
                <label for="price">Price:</label>
                <input type="number" id="price" class="form-control" v-model="editProductData.price" />
              </div>
              
            </template>
            <template #modal-footer>
              <b-btn class="primary" @click="submitEditProductForm(category, product)">Submit</b-btn>
              <b-btn @click="closeEditProductModal">Close</b-btn>
            </template>
          </b-modal>
        </div>
      </div>
      <div class="category-circle-container">
        <div class="category-circle" @click="openAddProductModal">
          <div class="category-plus-container">
            <div class="category-horizontal-plus"></div>
            <div class="category-vertical-plus"></div>
          </div>
        </div>
      </div>
      <b-modal id="add-product-circle-modal" v-model="showAddProductModal" size="lg" variant="primary" no-close-on-backdrop>
        <template #modal-header>
          <h3 class="mb-0">Add Product</h3>
        </template>
        <template #default>
          <div class="form-group">
            <div id="admin-product-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isAddSubmitButtonClicked" class="admin-product-error-message">
                <ul>
                    <template v-if="errorMessages.length > 0">
                      <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                    </template>
                    <template v-else-if="serverErrorMessages.length > 0">
                      <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                    </template>
                </ul>
            </div>
            <label for="name">Name:</label>
            <input type="text" id="name" class="form-control" v-model="addProductData.name" />
          </div>
          <div class="form-group">
            <label for="price">Price:</label>
            <input type="number" id="price" class="form-control" v-model="addProductData.price" />
          </div>
          
        </template>
        <template #modal-footer>
          <b-btn class="primary" @click="submitAddProductForm(category)">Submit</b-btn>
          <b-btn @click="closeAddProductModal">Close</b-btn>
        </template>
      </b-modal>
      <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
          :message="$store.state.notification.message" @clear-notification="clearNotification"/> 
    </div>
  </template>
  
  
  <script>
  import Notification from './Notification.vue'
  
  export default {
    name: 'ManagerProduct',
    props: {
      category: {
        type: Object,
        required: true
      }
    },
    components: {
      Notification
    },
    data() {
      return {
        showEditProductModal: false,
        showAddProductModal: false,
        addProductData: {
          id: null,
          name: "",
          price: null,
          rating: 0,
        },
        editProductData: {
          id: null,
          name: "",
          price: null,
          rating: 0,
        },
        errorMessages: [],
        serverErrorMessages: [],
        isAddSubmitButtonClicked: false,
        isEditSubmitButtonClicked: false
      }
    },
    methods: {
      clearNotification() {
        this.$store.commit('clearNotification');
      },
      openAddProductModal() {
        this.showAddProductModal = true;
      },
      closeAddProductModal() {
        this.showAddProductModal = false;
        this.addProductData = {
          id: null,
          name: "",
          price: null,
          rating: 0
        }
      },
      editProduct(product){
        this.showEditProductModal = true;
        this.editProductData = {
            id: product.id,
            name: product.name,
            price: product.price,
            rating: product.rating,
        };
      },
      closeEditProductModal(){
        this.showEditProductModal = false;
        this.editProductData = {
          id: null,
          name: "",
          price: null,
          rating: 0
        }
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
      validation(entity) {
        let message = 'Name cannot be empty'
        this.validateEachEntity(entity.name, message);
  
        message = 'Price cannot be empty';
        this.validateEachEntity(entity.price, message);
  
      },
      async submitAddProductForm(category) {
        this.isAddSubmitButtonClicked = true;
        this.validation(this.addProductData);
        if (this.errorMessages.length > 0) {
          return;
        }
        
        const user_id = parseInt(localStorage.getItem('userId')); 
        const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category/${category.id}/product_manager_api`, {
          method: "POST",
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            input_name: this.addProductData.name,
            input_price: this.addProductData.price
          })
        }).then(async result => {
          const data = await result.json();
          if (result.ok) {
            this.$store.commit('setNotification', { variant: 'success', message: data.message });
            const newProduct = {
              id: data.id, // Assuming the API returns the ID of the newly created show
              name: this.addProductData.name,
              price: this.addProductData.price,
              rating: 0
            };
            category.products.push(newProduct);
          }
          else {
            this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
          }
          this.closeAddProductModal();
        })
      },
      async submitEditProductForm(category, product){
        this.isEditSubmitButtonClicked = true;
        this.validation(this.editProductData);
        if (this.errorMessages.length > 0) {
          return;
        }
  
        if (this.editProductData.name === product.name && this.editProductData.price === product.price) {
          this.$store.commit('setNotification', { variant: 'info', message: 'No changes detected!' });
          this.closeEditProductModal();
          return; 
        }
  
        const user_id = parseInt(localStorage.getItem('userId')); 
        const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category/${category.id}/product_manager_api/${product.id}`, {
          method: "PUT",
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            input_name: this.editProductData.name,
            input_price: this.editProductData.price
          })
        }).then(async result => {
          const data = await result.json();
          if (result.ok) {
            this.$store.commit('setNotification', { variant: 'success', message: data.message });
            product.name = this.editProductData.name;
            product.price = this.editProductData.price;
          }
          else {
            this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
          }
          this.closeEditProductModal();
        })
      },
      async deleteProduct(category, product){
        const confirmDelete = window.confirm('Are you sure you want to delete this Product?');
        if (confirmDelete) {
          const user_id = parseInt(localStorage.getItem('userId')); 
          const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category/${category.id}/product_manager_api/${product.id}`, {
                      method: "DELETE",
                      headers: {
                          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                      },
                  }).then(async result => {
                      const data = await result.json();
                      if (result.ok) {
                          this.$store.commit('setNotification', { variant: 'success', message: data.message });
                          category.products = category.products.filter((s) => s.id !== product.id);
                      }
                      else {
                          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                      }
                  })
        }
      }
    }
  }
  
  </script>
  
  <style scoped>
  .category-circle-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 40%;
  }
  
  .category-circle, .product-circle {
    position: relative;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: rgb(44, 108, 128);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  
  .category-plus-container, .product-plus-container {
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
  
  #admin-product-error-message {
    width: 750px;
    margin-top: -15px;
    border-color: black; 
    border: 2px solid black;
  }
  
  #admin-product-error-message ul {
    color: white;
    background-color: lightcoral;
    padding: 10px;
    margin: 0;
    list-style-type: none;
  }
  #products-box {
      max-height: 235px; 
      overflow-y: auto; 
      margin-bottom: 10px;
    }
  
    #product-item {
      width: 100%;
      border: 1px solid #ccc;
      margin-bottom: 10px;
      background-color: lightcoral;
    }
  
    #product-actions {
      display: flex;
      justify-content: center;
      margin-bottom: 10px;
      margin-top: 10px;
    }
  
    #actions-message {
      text-align: center;
      /* Add other styling properties as needed */
    }
    #each-detail {
      display: flex;
      justify-content: space-between;
    }
    #product-actions .dropdown-button-color .dropdown-toggle{
      background-color: lightskyblue;
    }
    .left-details {
      padding-right: 10px;
    }
  
    .right-details {
      padding-left: 10px;
    }
  
  </style>