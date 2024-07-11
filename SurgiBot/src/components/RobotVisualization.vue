<template>

  <div>
    <div style="width: 245px; height: 40px; background-color: grey; opacity: 0.2;">
      <input type="file" id="file-selector" @change="handleFileChange" accept=".stl" single>
    </div>
    <div class="input-container">
      <input id="X"     placeholder="X" />
      <input id="Y"     placeholder="Y" />
      <input id="Z"     placeholder="Z" />
      <input id="Roll"  placeholder="Roll" />
      <input id="Pitch" placeholder="Pitch"/>
      <input id="Yaw"   placeholder="Yaw"  />
    </div>
  </div>

  <div ref="threeJsContainer" style="width: 100%; height: 400px;"></div>

  <div id="gui_container"></div>

  <v-select  
    density="compact"  
    :items="['input(simu)', 'input(real)', 'datGUI']"
    style="position: absolute; right: 0px; top: 0px; width: 245px;" v-model="selector">
  </v-select>

  <v-select
    id="objectSelector"  
    density="compact"
    chips  
    :items="objList"
    style="position: absolute; left: 0px; top: 45px; width: 245px;" v-model="objSelector">
  </v-select>
  
</template>

<style>
  #gui_container{
    position: absolute;
    top: 45px;
    right: 0px;
  }

  .input-container input {
  display: block;
  margin-bottom: 5px;
  width: 245px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  /* border: 1px black solid;
  color: rgba(0, 0, 0, 0.681); */
}

  .input-container {
    position: absolute;
    top: 90px;
  }

</style>


<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import Stats from 'three/examples/jsm/libs/stats.module'
import ThreejsTest from './ThreejsTest.vue';
import { GUI } from 'dat.gui';
import { TransformControls } from 'three/examples/jsm/controls/TransformControls.js';

import store from '../store/store.js';


const selector = ref("");
const threeJsContainer = ref(null);
const objSelector = ref();
const objList = ref([]);

let renderer;
let camera;
let material1;
let material2;
let material3;
let geometries;
let scene;
let cube;
let loader;
let control;
let material_stl;
let envTexture;
let light;
var mesh1;
var mesh2;
var mesh3;
var mesh4;
var mesh5;
var mesh6;
var axis1;
var axis2;
var axis3;
var axis4;
var axis5;
var axis6;
var gui;
var options
const scale = 0.02;
var transformControls;

const initCamera = function () {
  camera = new THREE.PerspectiveCamera(
    45,
    3.5 * window.innerWidth / window.innerHeight,
    0.2,
    1000
  );
  camera.position.z = 10;
  camera.position.x = 10;
  camera.position.y = 10;
};


const initRenderer = function () {
  scene = new THREE.Scene();
  scene.add(new THREE.AxesHelper(5)); // add three axis line

  // light = new THREE.SpotLight();
  // light.position.set(20, 20, 20);
  // scene.add(light);

  light = new THREE.DirectionalLight(0xffffff, 2.0);
  light.position.set(0.0, 0.3, 0.0);
  scene.add(light);

  
  
  renderer = new THREE.WebGLRenderer({ alpha: true });
  renderer.setSize(threeJsContainer.value.offsetWidth, threeJsContainer.value.offsetHeight);
  threeJsContainer.value.appendChild(renderer.domElement);

};

const addGrid = function () {
  const helper = new THREE.GridHelper(20, 20);
    helper.material.opacity = 0.25;
    helper.material.transparent = true;
    scene.add( helper );
}

const addtransformer = function () {
  transformControls = new TransformControls(camera, renderer.domElement);
}


const initGeometry = function () {
  control = new OrbitControls(camera, renderer.domElement); // control the view
  control.target.set(0, 0, 0);
  control.enableDamping = true;
  
  envTexture = new THREE.CubeTextureLoader().load([ ]); 
  envTexture.mapping = THREE.CubeReflectionMapping;


  material1 = new THREE.MeshPhysicalMaterial({
    color: 0xf0f0f0,
    metalness: 0.8,
    roughness: 0.2,
    envMapIntensity: 1,
    transmission: 0.5,  // you might want to adjust this for transparency effect
    transparent: true
  });

  material2 = new THREE.MeshPhysicalMaterial({
    color: 0xe0e0e0,
    metalness: 0.8,
    roughness: 0.2,
    envMapIntensity: 1,
    transmission: 0.5,  // you might want to adjust this for transparency effect
    transparent: true
  });

  material3 = new THREE.MeshPhysicalMaterial( { 
      color: 0x3D85C6,
      transparent: true,
      transmission: 1.0} );

  // get the x y z (L, H, W) of the mesh
  const Sizeof = function(mesh){
    const boundingBox = new THREE.Box3();
    boundingBox.setFromObject(mesh);
    // Calculate size
    const size = new THREE.Vector3();
    boundingBox.getSize(size);
    return size
  }

  //-------- add stl file --------
  loader = new STLLoader();

  // load mesh1
  loader.load('../../meshes/meca500/Meca500_axis1.STL', function (geometries) {
    mesh1 = new THREE.Mesh(geometries, material1);
    mesh1.scale.set(scale,scale,scale);
    mesh1.geometry.center();
    mesh1.position.set(0, Sizeof(mesh1).y/2, 0);
    scene.add(mesh1);
    // load axis1
    axis1 = new THREE.Object3D();
    axis1.translateZ(20.5);
    mesh1.add(axis1);
    // load mesh2
    loader.load(
      '../../meshes/meca500/Meca500_axis2.STL',
    function (geometries) {
        mesh2 = new THREE.Mesh(geometries, material2)
        // mesh2.scale.set(scale,scale,scale);
        mesh2.geometry.center();
        mesh2.position.set(0, 128.75*scale, 0);
        const mesh2PositionRelativeToMesh1 = mesh1.worldToLocal(mesh2.position.clone());
        // console.log(mesh2PositionRelativeToMesh1);
        mesh2.position.copy(mesh2PositionRelativeToMesh1);
        axis1.add(mesh2);
        // load axis2
        axis2 = new THREE.Object3D();
        axis2.translateY(44.5*scale);
        mesh2.add(axis2);
        // load mesh3 
        loader.load(
        '../../meshes/meca500/Meca500_axis3.STL',
        function (geometries) {
            mesh3 = new THREE.Mesh(geometries, material1)
            // mesh3.scale.set(scale, scale, scale);
            mesh3.geometry.center();
            mesh3.position.set(0,65.25,-4);
            axis2.add(mesh3)
            // load axis3
            axis3 = new THREE.Object3D();
            axis3.translateY(69.75);
            axis3.translateZ(4.0);
            mesh3.add(axis3);
            // load mesh4
            loader.load(
            '../../meshes/meca500/Meca500_axis4.STL',
            function (geometries) {
                mesh4 = new THREE.Mesh(geometries, material2);
                // mesh4.scale.set(scale,scale,scale);
                mesh4.geometry.center();
                mesh4.position.set(4, 10.13, 17.0);
                axis3.add(mesh4)

                // load axis4
                axis4 = new THREE.Object3D();
                axis4.translateY(24.88);
                axis4.translateZ(44.5);
                mesh4.add(axis4);
              
                //load mesh5
                loader.load(
                '../../meshes/meca500/Meca500_axis5.STL',
                function (geometries) {
                  mesh5 = new THREE.Mesh(geometries, material1);
                  // mesh5.scale.set(scale,scale,scale);
                  mesh5.geometry.center();
                  mesh5.position.set(-1.75, 0, 40.5);
                  axis4.add(mesh5)
                  // load axis5
                  axis5 = new THREE.Object3D();
                  axis5.translateZ(18);
                  mesh5.add(axis5);
                  loader.load(
                  '../../meshes/meca500/Meca500_axis6.STL',
                  function (geometries) {
                    mesh6 = new THREE.Mesh(geometries, material2);
                    // mesh6.scale.set(scale,scale,scale);
                    mesh6.geometry.center();
                    mesh6.position.set(7, 0, 24);
                    axis5.add(mesh6)
                  });

                });

            });
              
        });

    });

  });
  //-------- end stl file --------
  
}

function datGUI() {
  options = {
    mesh1: 0,
    axis1: 0,
    axis2: 0,
    axis3: 0,
    axis4: 0,
    axis5: 0,

  };
  // DAT.GUI Related Stuff
  gui = new GUI({ autoPlace: false });
  gui.domElement.id = 'gui';
  gui_container.appendChild(gui.domElement);
  gui.add(options, 'mesh1', -180, 180).listen();
  gui.add(options, 'axis1', -180, 180).listen();
  gui.add(options, 'axis2', -180, 180).listen();
  gui.add(options, 'axis3', -180, 180).listen();
  gui.add(options, 'axis4', -180, 180).listen();
  gui.add(options, 'axis5', -180, 180).listen();
}

function render() {
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}

var yAxis = new THREE.Vector3(0, 1, 0);
var xAxis = new THREE.Vector3(1, 0, 0);
var zAxis = new THREE.Vector3(0, 0, 1);

const animate = function () {
    requestAnimationFrame(animate);
    if (mesh1 && mesh2 && mesh3 && mesh4 && mesh5 && mesh6){
      switch (selector.value) {
        case "input(simu)":
        mesh1.setRotationFromAxisAngle(yAxis, store.state.joint[0] * Math.PI / 180);
        axis1.setRotationFromAxisAngle(yAxis, store.state.joint[1] * Math.PI / 180);
        axis2.setRotationFromAxisAngle(xAxis, store.state.joint[2] * Math.PI / 180);
        axis3.setRotationFromAxisAngle(xAxis, store.state.joint[3] * Math.PI / 180);
        axis4.setRotationFromAxisAngle(zAxis, store.state.joint[4] * Math.PI / 180);
        axis5.setRotationFromAxisAngle(xAxis, store.state.joint[5] * Math.PI / 180);
          break;
        case "datGUI":
          mesh1.setRotationFromAxisAngle(yAxis, options.mesh1 * Math.PI / 180);
          axis1.setRotationFromAxisAngle(yAxis, options.axis1 * Math.PI / 180);
          axis2.setRotationFromAxisAngle(xAxis, options.axis2 * Math.PI / 180);
          axis3.setRotationFromAxisAngle(xAxis, options.axis3 * Math.PI / 180);
          axis4.setRotationFromAxisAngle(zAxis, options.axis4 * Math.PI / 180);
          axis5.setRotationFromAxisAngle(xAxis, options.axis5 * Math.PI / 180);
          break;
        case "input(real)":
          mesh1.setRotationFromAxisAngle(yAxis, 0 * Math.PI / 180);
          axis1.setRotationFromAxisAngle(yAxis, store.state.joint_real[0] * Math.PI / 180);
          axis2.setRotationFromAxisAngle(xAxis, store.state.joint_real[1] * Math.PI / 180);
          axis3.setRotationFromAxisAngle(xAxis, store.state.joint_real[2] * Math.PI / 180);
          axis4.setRotationFromAxisAngle(zAxis, store.state.joint_real[3] * Math.PI / 180);
          axis5.setRotationFromAxisAngle(xAxis, store.state.joint_real[4] * Math.PI / 180);
          break;

        default:
          break
      }
      

      // mesh1.setRotationFromAxisAng
      
    }
    

    control.update();

    // cube.rotation.x += 0.01;
    // cube.rotation.y += 0.01;
    renderer.render(scene, camera);

  };


function handleFileChange(event) {
  console.log(Array.from(event.target.files)); // Convert FileList object to an array
  // Additional processing can be done here, like reading the files or uploading them
  const stl_import = event.target.files[0];

  if (!stl_import) {return;}

  const reader = new FileReader();

  reader.onload = function(e){
    const buffer = e.target.result;
    const geometry_import = loader.parse(buffer);
    const mesh_import = new THREE.Mesh(geometry_import, material3);
    mesh_import.name = stl_import.name;
    mesh_import.scale.set(scale, scale, scale);
    mesh_import.geometry.center();
    mesh_import.position.set(0,1,5);
    scene.add(mesh_import);
    // transformControls.attach(mesh_import);
    // scene.add(transformControls);
  }

  reader.readAsArrayBuffer(stl_import);

  // push back the mesh name to the selector list
  objList.value.push(stl_import.name);
  console.log(objList.value);
}


onMounted(() => {
  initCamera();
  initRenderer();
  addGrid();
  addtransformer();
  initGeometry();
  window.addEventListener('resize', onWindowResize, false);
  datGUI()
  animate();
});

onUnmounted(() => {
  // Perform any cleanup like stopping animation frame, disposing geometries, materials, etc.
});

</script>
