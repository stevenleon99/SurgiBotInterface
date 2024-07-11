<template>
    <div>
      <!-- Display the message from the API or a loading message -->
      <p>{{ msg }}</p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted, onBeforeUnmount} from 'vue';
  import config from '../../config/config.js';
  import { ref } from 'vue';

  const msg = ref("loading");
  let polling: number | null | undefined = null;
  // Function to fetch data from the FastAPI backend
  async function fetchData() {

    try {
      const response = await fetch(config.URLprefix + "/api");
      const data = await response.json();
      console.log(data);
      msg.value = data.message;
    } catch (error) {
      msg.value = "loading";
      console.log(error);
    } 
  }

  // Function to start polling
  const startPolling = () => {
      fetchData(); // Fetch data immediately
      polling = setInterval(fetchData, 5000); // Adjust the interval as needed
    };

  // Function to stop polling
  const stopPolling = () => {
    if (polling) {
      clearInterval(polling);
    }
  };

  onMounted(() => {
    startPolling();
  });

  onBeforeUnmount(() => {
    stopPolling();
  });



  // Fetch data on component mount
  onMounted(() => {
    fetchData();
  });

  </script>