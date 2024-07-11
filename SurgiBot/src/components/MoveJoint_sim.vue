<script setup lang="ts">
    // import { ref } from 'vue';
    // import config from '../../config/config.js';
    import store from '../store/store.js';

    // const jointvalue = ref('');
    // const responsemessage = ref(null);

    function handleSubmit(){
        const joint1 = document.getElementById('joint1').value ? document.getElementById('joint1').value: 0;
        const joint2 = document.getElementById('joint2').value ? document.getElementById('joint2').value: 0;
        const joint3 = document.getElementById('joint3').value ? document.getElementById('joint3').value: 0;
        const joint4 = document.getElementById('joint4').value ? document.getElementById('joint4').value: 0;
        const joint5 = document.getElementById('joint5').value ? document.getElementById('joint5').value: 0;
        const joint6 = document.getElementById('joint6').value ? document.getElementById('joint6').value: 0;
        store.commit("updatejoint", {joints: [joint1, joint2, joint3, joint4, joint5, joint6]});
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
    <p><label for="myText">Enter 6 Joint Angle</label></p>
    <p>[In Simulation Environment] </p> 
    <input style="border: 1px black solid; color: rgba(0, 0, 0, 0.681);" id="joint1" placeholder="mesh1(degree)"  required />
    <input style="border: 1px black solid; color: rgba(0, 0, 0, 0.681);" id="joint2" placeholder="joint1(degree)"  required />
    <input style="border: 1px black solid; color: rgba(0, 0, 0, 0.681);" id="joint3" placeholder="joint2(degree)"  required />
    <input style="border: 1px black solid; color: rgba(0, 0, 0, 0.681);" id="joint4" placeholder="joint3(degree)"  required />
    <input style="border: 1px black solid; color: rgba(0, 0, 0, 0.681);" id="joint5" placeholder="joint4(degree)"  required />
    <input style="border: 1px black solid; color: rgba(0, 0, 0, 0.681);" id="joint6" placeholder="joint5(degree)"  required />
    <v-btn variant="outlined" @click="handleSubmit">Move</v-btn>
</template>