<template>
    <div>
      <Home />
  
      <div class="search-container">
        <h1>Search Products</h1>
        <div class="search-input">
          <label for="price">Price:</label>
          <input type="text" id="price" v-model="searchPrice" />
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="searchName" />
          <b-btn variant="primary" @click="searchProducts">Search</b-btn>
        </div>
        <div class="shows-container">
            <template v-for="rowProducts in chunkArray(products, 3)">
                <div v-for="(product, index) in rowProducts" :key="index" class="show-item">
                <h2> {{product.name}}</h2>
                <p>Price : {{ product.price }}</p>
                </div>
            </template>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Home from './Home.vue'
  
  export default {
    name: 'SearchProduct',
    components: {
      Home
    },
    data() {
      return {
        products: [],
        searchName: "",
        searchPrice:""
      };
    },
    methods: {
      // ... Existing search methods ...
      chunkArray(arr, size) {
        // Helper method to split the array into groups of given size
        const chunkedArr = [];
        for (let i = 0; i < arr.length; i += size) {
          chunkedArr.push(arr.slice(i, i + size));
        }
        return chunkedArr;
      },
      async searchProducts() {
        const user_id = parseInt(localStorage.getItem('userId')); 
        const response = await fetch(`http://127.0.0.1:5000/search/user/${user_id}/products?input_name=${this.searchName}&input_price=${this.searchPrice}`, {
        method: "GET",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          "Content-Type": "application/json"
        }
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.products = data.products;
        }
        else {
          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
      })
      }
    }
  };
  </script>
  
  <style scoped>
  /* ... Existing styles ... */
  
  .show-row {
    width: 100%;
    display: flex;
    margin-bottom: 20px;
  }
  
  .show-item {
    width: calc(33.33% - 10px);
    padding: 10px;
    border: 1px solid #ccc;
    background-color: greenyellow;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* Add the margin property to create space between theatres */
    margin-right: 10px;
  }
  .search-container {
    padding: 20px;
  }
  
  .search-input {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .shows-container {
    display: flex;
    flex-wrap: wrap;
  }

  /* Add more custom styles as needed */
  </style>
