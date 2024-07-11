<template>
    <p>Test Vuex</p>
    <div>{{ text }}</div>
    <div>{{ replacebyvuex }}</div>
	<div>{{ returnjoint }}</div>
	<button style="border: 2px solid black; width: 50px;" @click="zeroJoint">+</button>
</template>

<script>
import store from '../store/store.js';

export default {
	data() {
		return {
			text: 'Text Tx',
			joint: '1,2,3,4,5,6'
		}
	},
    computed: { 
		replacebyvuex: () => store.state.count,
		returnjoint: () => store.state.joint,
	},
	methods: {
		zeroJoint: () => store.commit('updateJoint', {joints: [1,2,3,4,5,6]}),
	}
}

</script>