<template>
  <div ref="threeJsContainer" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import Stats from 'three/examples/jsm/libs/stats.module'

const threeJsContainer = ref(null);
let renderer;
let camera;
let materials;
let geometries;
let scene;
let cube;
let loader;
let control;
let material_stl;
let envTexture;
let light;
let mesh;

const initCamera = function () {
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 60;
  camera.position.x = 3;
  camera.position.y = 2;
};

const initRenderer = function () {
  scene = new THREE.Scene();
  scene.add(new THREE.AxesHelper(5)); // add three axis line

  light = new THREE.SpotLight();
  light.position.set(20, 20, 20);
  scene.add(light);
  
  renderer = new THREE.WebGLRenderer({ alpha: true });
  renderer.setSize(threeJsContainer.value.offsetWidth, threeJsContainer.value.offsetHeight);
  threeJsContainer.value.appendChild(renderer.domElement);

};

const initGeometry = function () {
  control = new OrbitControls(camera, renderer.domElement); // control the view
  control.enableDamping = true;
  
  geometries = new THREE.BoxGeometry();
  materials = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
  cube = new THREE.Mesh(geometries, materials);
  scene.add(cube);

  envTexture = new THREE.CubeTextureLoader().load([ ]); 
  envTexture.mapping = THREE.CubeReflectionMapping;

  materials = new THREE.MeshPhysicalMaterial({
      color: 0xb2ffc8,
      envMap: envTexture,
      metalness: 0.25,
      roughness: 0.1,
      opacity: 1.0,
      transparent: true,
      transmission: 0.99,
      clearcoat: 1.0,
      clearcoatRoughness: 0.25,
  });

  loader = new STLLoader();
  loader.load(
      '../../meshes/jig.stl',
      function (geometries) {
          mesh = new THREE.Mesh(geometries, materials)
          scene.add(mesh)
      },
      (xhr) => {
          console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
      },
      (error) => {
          console.log(error)
      }
  );
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

const animate = function () {
    requestAnimationFrame(animate);
    
    control.update();

    // cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    mesh.rotation.y += 0.01;
    renderer.render(scene, camera);

  };


onMounted(() => {
  initCamera();
  initRenderer();
  initGeometry();
  window.addEventListener('resize', onWindowResize, false);
  animate();
})

onUnmounted(() => {
  // Perform any cleanup like stopping animation frame, disposing geometries, materials, etc.
});
</script>
