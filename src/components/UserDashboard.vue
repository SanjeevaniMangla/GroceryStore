<template>
    <div>
      <Home />
  
      <div class="categories-container">
        <!-- Loop through each Category -->
        <div v-for="category in categories" :key="category.id" class="category-box">
          <h2>{{ category.name }}</h2>
          <div class="shows-container">
            <!-- Loop through each group of three shows in the category.products_under_category array -->
            <div v-for="productGroup in chunkArray(category.products, 3)" :key="productGroup[0].id" class="show-row">
              <!-- Display three products in each row -->
              <div v-for="product in productGroup" :key="product.id" class="show-item">
                <!-- Display product details -->
                <div class="show-details">
                  <p><strong>Product Name:</strong> {{ product.name }}</p>
                  <p><strong>Price:</strong> {{ product.price }}</p>
                  <b-btn class="success"  @click="openBookingModal(category, product)">Order</b-btn>
                  
                  <b-modal id="user-book-modal" v-model="showBookingModal" size="lg" variant="primary" no-close-on-backdrop>
                    <template #modal-header>
                      <h3 class="mb-0">Order</h3>
                    </template>
                    <template #default>
                      <div class="form-group">
                        <div id="user-book-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isSubmitButtonClicked" class="user-book-error-message">
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
                        <label for="number-of-products">Number of Products:</label>
                        <input type="number" id="number-of-products" class="form-control" v-model="numberOfProducts" />
                      </div>
                      <div class="form-group">
                        <label for="price">Price:</label>
                        <input type="number" id="price" class="form-control" v-model="price" disabled/>
                      </div>
                      <div class="form-group">
                        <label for="total_price">Total Price:</label>
                        <input type="number" id="total_price" class="form-control" v-model="totalPrice" disabled/>
                      </div>
                    </template>
                    <template #modal-footer>
                      <b-btn class="primary" @click="submitBooking(category, product)">Confirm Order</b-btn>
                      <b-btn @click="closeBookingModal">Close</b-btn>
                    </template>
                  </b-modal>
                  <!-- Add more show details as needed -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
          :message="$store.state.notification.message" @clear-notification="clearNotification"/>
    </div>
  </template>
  
  <script>
  import Home from './Home.vue'
  import Notification from './Notification.vue'
  
  export default {
    name: 'UserDashboard',
    components: {
      Home,Notification
    },
    data() {
      return {
        categories: [],
        errorMessages: [],
        serverErrorMessages: [],
        isSubmitButtonClicked: false,
        showBookingModal: false,
        numberOfProducts: 0,
        totalPrice: 0,
        price: 0,
        currentCategory: null,
        currentProduct: null,
      };
    },
    created() {
      this.fetchCategories();
    },
    watch: {
      numberOfProducts: function(newValue) {
        // Calculate the total price by multiplying the number of products with the product price.
        this.totalPrice = newValue * this.price;
      }
    },
    methods: {
      clearNotification() {
              this.$store.commit('clearNotification');
          },
      openBookingModal(category, product){
        this.currentCategory= category; // Store the current theatre
        this.currentProduct = product; 
        this.showBookingModal = true;
        const bookedProducts = category.bookings.reduce((totalProducts, booking) => totalProducts + booking.number_of_products, 0);
        this.price = product.price;
  
      },
      closeBookingModal(){
        this.showBookingModal = false;
        this.price = 0;
        
      },
      async fetchCategories() {
        const user_id = parseInt(localStorage.getItem('userId'));
        const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category_api`, {
          method: 'GET',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        });
  
        const data = await response.json();
        if (response.ok) {
          this.categories = data.categories;
        } else if (response.status === 409) {
          // Handle conflict
        } else {
          this.$store.commit('setNotification', {
            variant: 'error',
            message: 'Something went wrong. Try again!!!',
          });
        }
      },
      chunkArray(arr, size) {
        // Helper method to split the array into groups of given size
        const chunkedArr = [];
        for (let i = 0; i < arr.length; i += size) {
          chunkedArr.push(arr.slice(i, i + size));
        }
        return chunkedArr;
      },
      validation() {
  
        let message = 'Number of products cannot be 0 or empty'
        if (this.errorMessages.includes(message)) {
          let indexOFMessage = this.errorMessages.indexOf(message);
          this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
          if (this.numberOfProducts === null || this.numberOfProducts === 0 || this.numberOfProducts === "") {
            this.errorMessages.splice(indexOFMessage, 0, message);
          }
        }
        else {
          if (this.numberOfProducts === null || this.numberOfProducts === 0 || this.numberOfProducts === "") {
            this.errorMessages.push(message);
          }
        }
  
      },
      async submitBooking(category, product){
        this.isSubmitButtonClicked = true;
  
        this.validation();
        if (this.errorMessages.length > 0) {
          return;
        }
        const user_id = parseInt(localStorage.getItem('userId'));
        const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category/${this.currentCategory.id}/product/${this.currentProduct.id}/booking_api`, {
          method: "POST",
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            total_price: this.totalPrice,
            number_of_products: this.numberOfProducts
          })
        }).then(async result => {
          const data = await result.json();
          if (result.ok) {
            this.$store.commit('setNotification', { variant: 'success', message: data.message });
            await this.fetchCategories();
          }
          else {
            this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
          }
          this.closeBookingModal();
        })
      }
    },
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here */
  .categories-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .category-box {
    width: 100%;
    margin: 10px;
    padding: 20px;
    border: 2px solid red;
    background-color: yellow;
  }
  
  .shows-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    height: 245px;
    overflow-y: auto;
  }
  
  .show-row {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }
  
  .show-item {
    width: calc(33.33% - 20px);
    margin: 10px;
    padding: 10px;
    border: 4px solid blue;
    background-color: greenyellow;
  }
  #user-book-error-message {
    width: 750px;
    margin-top: -15px;
    border-color: black; 
    border: 2px solid black;
  }
  
  #user-book-error-message ul {
    color: white;
    background-color: lightcoral;
    padding: 10px;
    margin: 0;
    list-style-type: none;
  }
  
  </style>