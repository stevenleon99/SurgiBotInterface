<script setup lang="ts">
    import { ref } from 'vue';
    import config from '../../config/config.js';

    const Pose = ref('');
    const responsemessage = ref(null);

    function handleSubmit(){
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "pose": Pose.value})
        };

        fetch(config.URLprefix+'/api/movePose', requestOptions)
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
        <p><label for="myText">Enter Pose (x y z rx ry rz)</label></p> 
        <input style="color: rgba(0, 0, 0, 0.681);" type="text" id="myText" name="myText" placeholder="[200, 0, 320, 0, 90, 0]" v-model="Pose" required>
        <v-btn type="submit" variant="outlined">Move</v-btn>
        <p>Pose entered is: {{ Pose }}</p>
        <p>{{responsemessage}}</p>
    </form>
</template>