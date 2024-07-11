<template>
  <v-container fluid>
    <v-row justify="space-between">
      <v-col cols="12" md="4" >
        <v-card class="centered-content 
        d-flex flex-column 
        align-center 
        justify-center">
          <!-- Card content -->
          <StatusTable></StatusTable>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="centered-content 
        d-flex flex-column 
        align-center 
        justify-center">
          <!-- Card content -->
          <MoveJoint_sim></MoveJoint_sim>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="centered-content 
        d-flex flex-column 
        align-center 
        justify-center">
          <!-- Card content -->
          <Header></Header>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="space-between">
      <v-col cols="12" md="4" >
        <v-card class="centered-content 
        d-flex flex-column 
        align-center 
        justify-center">
          <!-- Card content -->
          <MoveJoint></MoveJoint>
          <!-- <ThreejsTest /> -->
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="centered-content 
        d-flex flex-column 
        align-center 
        justify-center">
          <!-- Card content -->
          <!-- <Test></Test> -->
          <MovePose></MovePose>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="centered-content 
        d-flex flex-column 
        align-center 
        justify-center">
          <!-- Card content -->
          <JogInterface></JogInterface>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="space-between" style="height: 400px;">
      <v-col cols="12" md="12">
        <v-card class="centered-content 
        d-flex flex-column" style="height: 400px;">
          <!-- Card content -->
          <RobotVisualization />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </template>

<style>
    .centered-content {
    height: 245px; /* Set a height to see the vertical centering */
    }

</style>

<script setup>
import Header from "./Header.vue"
import StatusTable from "./StatusTable.vue"
import MoveJoint from "./MoveJoint.vue"
import ThreejsTest from "./ThreejsTest.vue";
import RobotVisualization from "./RobotVisualization.vue";
import MoveJoint_sim from "./MoveJoint_sim.vue";
import Test from "./Test.vue";
import MovePose from "./MovePose.vue"
import JogInterface from "./JogInterface.vue"
</script>


