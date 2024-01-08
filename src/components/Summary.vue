<template>
    <div>
        <Home/>
        <div class="summary-container">
            <h1>Select Category</h1>
            <div class="search-input">
                <b-dropdown id="category-dropdown" :text="current_category ? current_category.name : 'Select Category'" variant="outline-success">
                    <b-dropdown-item v-for="category in categories" :key="category.id" :value="category.name" @click="selectCategory(category)">
                        {{ category.name }}
                    </b-dropdown-item>
                </b-dropdown>
            </div>
            <br/>
            <br/>
            <div v-if="showImages" class="summary-images">
                <div class="image-container">
                    <img src="../assets/summary/category_1_products_sold.png" class="image" />
                </div>
                <div class="image-container">
                    <img src="../assets/summary/category_1_average_ratings.png" class="image" />
                </div>
                <div class="image-container">
                    <img src="../assets/summary/category_total_prices.png" class="image" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Home from './Home.vue'
import Notification from './Notification.vue'
import { BDropdown, BDropdownItem } from 'bootstrap-vue';

export default {
    name: 'Summary',
    components: {
        Home, Notification, BDropdown, BDropdownItem
    },
    data() {
        return {
            categories: [],
            current_category: null,
            productsSoldImage: '',
            averageRatingsImage: '',
            totalPricesImage: '',
            showImages: false,
            averageRatingsImageName: ''
        };
    },
    mounted(){ 
        this.fetchCategories(); 
    },
    methods: {
        async fetchCategories() {
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category_api`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    this.categories = data.categories;
                }
                else if (result.status === 409) {

                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
            })
        },
        async selectCategory(category) {
            this.showImages=false;
            this.current_category = category;
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category/${this.current_category.id}/summary_api`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            });
            if (response.ok) {
                this.showImages = true;
            }
            else if (result.status === 409) {

            }
            else {
                this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
            }
        },
    }
}


</script>

<style >

.summary-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    height: 100vh;
    padding-top: 20px;
}

.search-input {
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
}

.summary-images {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.image-container {
    margin: 10px;
    border: 1px solid #ccc; /* Add border to the image container */
}

.image {
    max-width: 100%;
    height: auto;
    border: 5px solid #dd1313; /* Add border to the image */
}


</style>