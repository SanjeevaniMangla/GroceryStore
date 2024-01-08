<template>
    <div>
        <Home />
        <div class="bookings-container">
            <div v-for="(booking, index) in bookings" :key="index" class="booking-card">
                <div class="booking-info">
                    <div class="booking-row">
                        <div class="left-info">
                            Number of Products: {{ booking.number_of_products }}
                        </div>
                        <div class="center-info">
                            Total Price: {{ booking.total_price }}
                        </div>
                        <div class="right-info">
                        </div>
                    </div>
                    <div class="booking-row">
                        <div class="left-info">
                            
                        </div>
                        <div class="center-info">
                            
                        </div>
                        <div class="right-info">
                            <b-button v-if="!booking.is_rating_given" @click="openratingModal(booking)" variant="primary" class="rate-button">Rate</b-button>
                            <b-modal id="rating-modal" v-model="showRatingModal" size="sm" title="Rating" no-close-on-backdrop>
                                <div id="rating-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isSubmitButtonClicked" class="category-error-message">
                                    <ul>
                                        <template v-if="errorMessages.length > 0">
                                            <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                                        </template>
                                        <template v-else-if="serverErrorMessages.length > 0">
                                            <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                                        </template>
                                    </ul>
                                </div>
                                <label for="rating">Rating (out of 10):</label>
                                <input type="number" id="rating" class="form-control" v-model="rating" />
                                <template #modal-footer>
                                    <b-button class="primary" v-on:click="submitRating()">Submit</b-button>
                                    <b-button @click="closeRatingModal">Close</b-button>
                                </template>
                            </b-modal>
                        </div>
                    </div>
                    <div class="booking-row">
                        <div class="left-info">
                            Product Name: {{ booking.product_name }}
                        </div>
                        <div class="center-info">
                            Category Name: {{ booking.category_name }}
                        </div>
                        <div class="right-info">
                            <!-- Empty space for better alignment -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import Home from './Home.vue'
import Notification from './Notification.vue'

export default {
    name: 'Bookings',
    components: {
        Home, Notification
    },
    data() {
        return {
            bookings: [],
            current_booking: null,
            showRatingModal: false,
            rating: null,
            errorMessages: [],
            serverErrorMessages: [],
            isSubmitButtonClicked: false
        };
    },
    mounted() {
        this.fetchBookings();
    },
    methods: {
        openratingModal(booking){
            this.showRatingModal = true
            this.current_booking = booking;
        },
        closeRatingModal(){
            this.showRatingModal = false;
            this.current_booking = null;
        },
        async submitRating(){
            this.isSubmitButtonClicked = true;
            let message = "Rating is not valid";
            if (this.errorMessages.includes(message)) {
                if(this.rating === null || this.rating === "" || this.rating === undefined || this.rating < 0 || this.rating > 10){
                    return;
                }
                else{
                    this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
                }
            }
            else{
                if(this.rating === null || this.rating === "" || this.rating === undefined || this.rating < 0 || this.rating > 10){
                    this.errorMessages.push(message);
                }
                else{
                    
                }
            }
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category/${this.current_booking.category_id}/product/${this.current_booking.product_id}/booking/${this.current_booking.id}/rating_api`, {
                method: "POST",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    rating: this.rating
                })
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    this.bookings = data;
                    this.$store.commit('setNotification', { variant: 'success', message: 'Rating has been successfully given!!!' });
                    this.closeRatingModal();
                    await this.fetchBookings();
                }
                else if (result.status === 409) {

                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
            })
        },
        async fetchBookings() {
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/booking_api`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    this.bookings = data;
                }
                else if (result.status === 409) {

                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
            })
        }
    }
}
</script>

<style>
.bookings-container {
    display: flex;
    flex-wrap: wrap;
    max-height: 1000px; 
    overflow-y: auto;
}

.booking-card {
    border: 1px solid #ccc;
    margin: 10px;
    width: 100%;
    background-color: rgb(200, 223, 68);
}

.booking-info {
    padding: 10px;
}

.left-info {
    flex: 1;
}

.center-info {
    flex: 1;
    text-align: center;
}

.booking-row {
    display: flex;
    justify-content: space-between;
    background-color: rgb(97, 224, 97);
    align-items: center; /* Align items vertically in the center */
}

.right-info {
    flex: 1;
    text-align: right;
}

.rate-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px; /* Increase padding for wider button */
    cursor: pointer;
    border-radius: 4px;
    transition: background-color 0.3s ease;
    width: 100px;
}

.rate-button:hover {
    background-color: #0056b3;
}
#rating-error-message {
  width: 265px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#rating-error-message ul {
  color: white;
  background-color: lightcoral;
  padding: 10px;
  margin: 0;
  list-style-type: none;
}
</style>