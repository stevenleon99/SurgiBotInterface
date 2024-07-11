<script setup lang="ts">
    import { ref } from 'vue';
    import config from '../../config/config.js';

    const joint = ref('');
    const responsemessage = ref('');

    function handleSubmit(){
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "joint": joint.value})
        };
        responsemessage.value = "[SurgiBot Frontend]: sending msg and moving";
        fetch(config.URLprefix+'/api/moveJoint', requestOptions)
            .then(response => response.json()) // Convert to JSON
            .then(data => responsemessage.value = data.message)
            .catch(error => console.error('Error:', error));
    }
</script>

<style>
.form-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
</style>

<template>
    <form class="form-container" id="myForm" @submit.prevent="handleSubmit">
        <p><label for="myText">Enter 6 Joint Angle</label></p> 
        <input style="color: rgba(0, 0, 0, 0.681);" type="text" id="myText" name="myText" placeholder="[0,90,0,0,-90,0]" v-model="joint" required>
        <v-btn type="submit" variant="outlined">Move</v-btn>
        <p>Joint entered is: {{ joint }}</p>
    </form>
</template>