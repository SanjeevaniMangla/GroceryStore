<template>
    <div  :class="['notification', variant]">
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Notification',
    props: {
      variant: {
        type: String,
        default: 'success' // Default variant is success, but you can customize it
      },
      message: {
        type: String,
        required: true
      }
    },
    mounted() {
      // Automatically hide the notification after a delay (e.g., 3000 milliseconds)
      setTimeout(() => {
        this.$emit('clear-notification'); // Emit clear-notification event after timeout
      }, 3000);
    }
  };
  </script>
  
  <style scoped>
  .notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px;
    border-radius: 4px;
    color: #fff;
  }
  
  .success {
    background-color: rgb(32, 204, 32);
  }
  
  .error {
    background-color: red;
  }

  .warning {
    background-color: yellow;
  }

  .info{
    background-color: rgb(34, 89, 207);
  }
  </style>