<template>
    <div>
      <Home />
  
      <div class="search-container">
        <h1>Search Category</h1>
        <div class="search-input">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="searchName" />
          <b-btn variant="primary" @click="searchCategories">Search</b-btn>
        </div>
        <!-- ... Existing search box and search button code ... -->
  
        <div class="categories-container">
    <template v-for="rowCategories in chunkArray(categories, 3)">
      
        <div v-for="(category, index) in rowCategories" :key="index" class="category-item">
          <img class="show-image" :src="getImageUrl(category.image)" />
          <h2> {{category.name}}</h2>
        
      </div>
    </template>
  </div>
      </div>
    </div>
  </template>
  
  <script>
  import Home from './Home.vue'
  
  export default {
    name: 'SearchCategory',
    components: {
      Home
    },
    data() {
      return {
        categories: [],
        searchName: ""
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
      getImageUrl(imagePath) {
            return require(`../assets/images/${imagePath}`)
        },
      async searchCategories() {
        const user_id = parseInt(localStorage.getItem('userId')); 
        const response = await fetch(`http://127.0.0.1:5000/search/user/${user_id}/categories?input_name=${this.searchName}`, {
        method: "GET",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          "Content-Type": "application/json"
        }
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.categories = data.categories;
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
  
  .category-row {
    width: 100%;
    display: flex;
    margin-bottom: 20px;
  }
  
  .category-item {
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
  
  .categories-container {
    display: flex;
    flex-wrap: wrap;
  }
  .show-image{
    width: 420px;
    height: 220px;
  }

  /* Add more custom styles as needed */
  </style>