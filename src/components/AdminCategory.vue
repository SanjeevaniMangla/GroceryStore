<template>
    <div>
        <div class="d-flex justify-content-between">
            <b-btn variant="primary" @click="editCategory(category)">Edit Category</b-btn>
            <b-modal id="edit-admin-category-modal" v-model="showEditModal" size="lg" variant="primary" no-close-on-backdrop>
            <template #modal-header>
                <h3 class="mb-0">Edit Category</h3>
            </template>
            <template #default>
                <div class="form-group">
                    <div id="admin-category-error-message"
                        v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isEditSubmitButtonClicked"
                        class="category-error-message">
                        <ul>
                            <template v-if="errorMessages.length > 0">
                                <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                            </template>
                            <template v-else-if="serverErrorMessages.length > 0">
                                <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{
                                    serverErrorMessage }}</li>
                            </template>
                        </ul>
                    </div>
                </div>
                <div class="form-group">
                    <label for="name">Edit Name:</label>
                    <input type="text" id="input_name" class="form-control" v-model="editCategoryData.name" />
                </div>
                <div class="form-group">
                    <label for="image">Image:</label>
                    <!-- <input type="file" id="image" class="form-control-file" @change="handleImageUpload" /> -->
                    <img :src="getImageUrl(category.image)" class="modal-image" />
                </div>
            </template>
            <template #modal-footer>
                <b-btn class="primary" @click="submitEditForm(category)">Submit</b-btn>
                <b-btn @click="closeEditModal">Close</b-btn>
            </template>
        </b-modal>
            <b-btn variant="danger" @click="deleteCategory(category)">Delete Category</b-btn>
        </div>
        <div class="text-center">
            <b-btn variant="success" @click="exportCategoryData(category)">Export Category Data</b-btn>
        </div>
        <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant"
            :message="$store.state.notification.message" @clear-notification="clearNotification" />
    </div>
</template>

<script>
import Notification from './Notification.vue'

export default {
    name: 'AdminCategory',
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
            showEditModal: false,
            editCategoryData: {
                id: null,
                name: "",
                image: null
            },
            errorMessages: [],
            serverErrorMessages: [],
            isEditSubmitButtonClicked: false
        }
    },
    methods: {
        clearNotification() {
            this.$store.commit('clearNotification');
        },
        async fetchCategory(category_id) {
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category_api/${category_id}`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    this.editCategoryData = data
                }
                else if (result.status === 409) {

                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
            })
        },
        getImageUrl(imagePath) {
            return require(`../assets/images/${imagePath}`)
        },
        editCategory(category) {
            // Set the data of the selected category to the editCategoryData property
            this.editCategoryData = {
                id: category.id,
                name: category.name,
                image: null, // We don't update the image here, it will be updated later if changed
            };

            // Open the edit modal
            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
            this.editCategoryData = {
                id: null,
                name: "",
                image: null,
            };
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
            this.validateEachEntity(this.editCategoryData.name, message);
        },
        async submitEditForm(category) {
            this.isEditSubmitButtonClicked = true;
            this.validation();
            if (this.errorMessages.length > 0) {
                return;
            }
            const formData = new FormData();

            if (this.editCategoryData.name !== category.name) {
                formData.append("input_name", this.editCategoryData.name);
            }

            if (formData.keys().next().done) {
                // No data in formData, so skip the API call
                this.closeEditModal();
                return;
            }
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category_api/${category.id}`, {
                method: "PUT",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                },
                body: formData,
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    category.id = data.id;
                    category.name = data.name;
                    category.image = data.image;
                    this.$store.commit('setNotification', { variant: 'success', message: data.message });
                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
                this.closeEditModal();
            })
        },
        async deleteCategory(category) {
            const confirmDelete = window.confirm('Are you sure you want to delete this category?');
            if (confirmDelete) {
                const user_id = parseInt(localStorage.getItem('userId'));
                const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category_api/${category.id}`, {
                    method: "DELETE",
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    },
                }).then(async result => {
                    const data = await result.json();
                    if (result.ok) {
                        this.$emit('category-deleted', category.id);
                        category = null;

                        this.$store.commit('setNotification', { variant: 'success', message: data.message });
                    }
                    else {
                        this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                    }
                })
            }
        },
        async exportCategoryData(category) {
            const user_id = parseInt(localStorage.getItem('userId'));
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/category/${category.id}/generate-csv`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            });

            if (response.ok) {
                const data = await response.json();

                // Poll for task status every 3 seconds
                let interval = setInterval(async () => {
                    const statusResponse = await fetch(`http://127.0.0.1:5000/user/${user_id}/check-state/${data.Task_ID}`, {
                        method: "GET",
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                        }
                    });

                    if (statusResponse.ok) {
                        const statusData = await statusResponse.json();

                        if (statusData.Task_State === 'SUCCESS') {
                            clearInterval(interval);

                            // Download the CSV file using the Flask API endpoint
                            const downloadResponse = await fetch(`http://127.0.0.1:5000/user/${user_id}/download-file`, {
                                method: "GET",
                                headers: {
                                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                                }
                            });

                            if (downloadResponse.ok) {
                                // Trigger the download by creating an anchor element and clicking it
                                const blob = await downloadResponse.blob();
                                const url = URL.createObjectURL(blob);

                                const downloadLink = document.createElement('a');
                                downloadLink.href = url;
                                downloadLink.download = 'data.csv';
                                downloadLink.click();
                                this.$store.commit('setNotification', { variant: 'success', message: 'File download' });
                            }
                            else {
                                this.$store.commit('setNotification', { variant: 'error', message: 'Error downloading file: Try again!!' });
                            }
                        }
                        else {
                            this.$store.commit('setNotification', { variant: 'info', message: 'Downloading is in progress!!' });
                        }
                    }
                }, 3000);
            } else {
                this.$store.commit('setNotification', { variant: 'error', message: 'Error in generating file: Try again!!' });
            }
        }
    },
}

</script>

<style scoped>
.modal-image {
    max-width: 100%;
    max-height: 400px;
    margin: auto;
    display: block;
}

#admin-category-error-message {
    width: 750px;
    margin-top: -15px;
    border-color: black;
    border: 2px solid black;
}

#admin-category-error-message ul {
    color: white;
    background-color: lightcoral;
    padding: 10px;
    margin: 0;
    list-style-type: none;
}
</style>