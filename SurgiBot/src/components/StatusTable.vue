<style>
    .circle {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
    }
    .red {
        background-color: red;
    }
    .green {
        background-color: green;
    }

    .myTable {
        width: 100%; /* Adjust as needed */
        height: 100%;
        border: 1px;
    }

    td {
        width: 25%;
    }
    .monitorBtn {
        position: absolute; 
        left: 0; 
        top: 0;
        
    }

</style>

<template>
    <div class="monitorBtn">
        <v-btn style="margin-right: 4px;"
            density="compact"
            @click="connect">Monitor</v-btn>
        <v-btn style="margin-right: 4px;"
            density="compact"
            @click="disconnect">Stop_Monitor</v-btn>
        <v-btn 
            density="compact"
            @click="deactivate">deactivate</v-btn>
    </div>
    
    <!-- <p>{{ messages }}</p> -->
    <v-container>
        <div class="text-center">Status Table</div>
        <table class="myTable"> <!-- Adds a border to the table -->
            <tr>
                <td>Robot Arm</td>
                <td id="robotarm_status" class="circle red"></td>
                <td>Joint1</td>
                <td>{{joint[0]}}</td>
            </tr>
            <tr>
                <td>MicroManipulator</td>
                <td class="circle red"></td>
                <td>Joint2</td>
                <td>{{joint[1]}}</td>
            </tr>
            <tr>
                <td>deck</td>
                <td class="circle red"></td>
                <td>Joint3</td>
                <td>{{joint[2]}}</td>
            </tr>
            <tr>
                <td>PinPoint</td>
                <td class="circle red"></td>
                <td>Joint4</td>
                <td>{{joint[3]}}</td>
            </tr>
            <tr>
                <td>Tool1</td>
                <td class="circle red"></td>
                <td>Joint5</td>
                <td>{{joint[4]}}</td>
            </tr>
            <tr>
                <td>Tool2</td>
                <td class="circle red"></td>
                <td>Joint6</td>
                <td>{{joint[5]}}</td>
            </tr>
        </table>
    </v-container>

</template>


<script>
import store from '../store/store.js';
import config from '../../config/config.js';

export default {
  data() {
    return {
      messages: "",
      websocket: null,
      joint: [0,0,0,0,0,0,0],
      polling: null,
    };
  },

//   mounted() {
//     this.startPolling();
//   },
//   beforeUnmount() {
//     this.stopPolling();
//   },

  methods: {
    handleMessage(event) {
      // Push the received message to the messages array
      //   this.messages.push(event.data);
        const str = event.data.split(null);
        const str_p = str[0].split("\u0000");
        let k = "";
        for (const item of str_p){
            if (item.includes("2026")){  // find the joints from the msg
                k = item;
                break;
            }
        }
        const jointVals = k.slice(7, -1);
        const jointArr = jointVals.split(",").map(Number);

        let robotStatus = document.getElementById("robotarm_status");
        robotStatus.classList.remove("red");
        robotStatus.classList.add("green");

        for (let idx=0; idx<jointArr.length; idx++){
           this.joint[idx] = jointArr[idx];
        }
        
        store.commit("updatejoint_real", {joints: this.joint});
    },

    connect() {
        // Connect to WebSocket server
        // this.websocket = new WebSocket('ws://127.0.0.1:8000/ws');
        this.websocket = new WebSocket('http://192.168.0.100:10001/')
        this.websocket.onmessage = this.handleMessage;
        console.log(this.messages);
            
    },

    disconnect() {
        
        if (this.websocket != null){
            let robotStatus = document.getElementById("robotarm_status");
            robotStatus.classList.remove("green");
            robotStatus.classList.add("red");
            
            console.log("[StatusTable]: Disconnect WebSocket")
            this.websocket.close();
        }
    },

    async deactivate() {
        try {
            const response = await fetch(config.URLprefix + "/robot/deactivate");
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.log(error);
        }
    }

    // -------- polling solution --------- 
    // handleMessage_pl(data) {
    //   // Push the received message to the messages array
    //   //   this.messages.push(event.data);

    //     let robotStatus = document.getElementById("robotarm_status");
    //     robotStatus.classList.remove("red");
    //     robotStatus.classList.add("green");

    //     this.messages = data.message;
    //     const joints = JSON.parse(this.messages)
    //     for (let idx=0; idx<joints.length; idx++){
    //        this.joint[idx] = joints[idx];
    //     }
        
    //     store.commit("updatejoint_real", {joints: this.joint});
    // },

    // async fetchdata() {
    //     try {
    //         const response = await fetch(config.URLprefix + "/robot/getjoints");
    //         const data = await response.json();
    //         this.handleMessage_pl(data)
    //     } catch (error) {
    //         console.log(error);
    //     }
    // },

    // startPolling() {
    //   this.fetchdata(); // Fetch data immediately
    //   this.polling = setInterval(this.fetchdata, 5000); // Adjust the interval as needed
    // },
    // stopPolling() {
    //     if (this.polling) {
    //     clearInterval(this.polling);
    //     }
    // }
    // -------- polling solution end --------- 

    
  },

};
</script>

