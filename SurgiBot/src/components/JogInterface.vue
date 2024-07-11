<template>
    <div class="button-grid">
      <v-btn @click="handleButtonClick('Z+')" class="arrow-button Z+ custom-size"><img src="../../asset/Z+.png"></v-btn>
      <v-btn @click="handleButtonClick('X-')" class="arrow-button X- custom-size"><img src="../../asset/X-.png"></v-btn>
      <v-btn @click="handleButtonClick('Z-')" class="arrow-button Z- custom-size"><img src="../../asset/Z-.png"></v-btn>
      <v-btn @click="handleButtonClick('Y+')" class="arrow-button Y+ custom-size"><img src="../../asset/Y+.png"></v-btn>
      <input style="color: rgba(0, 0, 0, 0.681); height: 60px; width: 100px;" type="text" id="myText" name="myText" placeholder="step size"  v-model="step">
      <v-btn @click="handleButtonClick('Y-')" class="arrow-button Y- custom-size"><img src="../../asset/Y-.png"></v-btn>
      <span></span>
      <v-btn @click="handleButtonClick('X+')" class="arrow-button X+ custom-size"><img style="width: 70px;" src="../../asset/X+.png"></v-btn>
      <span></span>
      <p style="position: absolute; left: 0px; bottom: 0px;">{{responsemessage}}</p>
      
    </div>
    
  </template>
  

  
  <script setup lang="ts">
  
    import { ref } from 'vue';
    import config from '../../config/config.js';

    const step = ref(10);
    const responsemessage = ref('');

    function handleButtonClick(buttonName:string){
      console.log("button is clicked", buttonName);
      console.log("the step is", step.value);
      if (step.value != ''){
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "jog_dir": buttonName, "jog_step": step.value})
        };
        responsemessage.value = "[SurgiBot Frontend]: sending msg and moving";
        fetch(config.URLprefix+'/api/jog', requestOptions)
            .then(response => response.json()) // Convert to JSON
            .then(data => responsemessage.value = data.message)
            .catch(error => console.error('Error:', error));
      } else {
        responsemessage.value = "[SurgiBot Frontend]: step input empty";
      }
    }
      
  </script>
  

  <style scoped>
  .button-grid {
    align-items: center;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  
  .arrow-button {
    border: none;
    background: none;
  }
  
  .arrow-button img {
    width: 50px; /* Adjust as needed */
    height: 50px;
  }

  .custom-size {
    width: 100px; /* Custom width */
    min-height: 60px;
  }

  </style>