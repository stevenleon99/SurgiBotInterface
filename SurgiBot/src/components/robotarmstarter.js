import * as THREE from 'three';
import { GUI } from 'dat.gui';

var scene = new THREE.Scene();


// Camera
var aspect = window.innerWidth / window.innerHeight;
var camera = new THREE.PerspectiveCamera( 60, aspect, 0.1, 1000 );
camera.position.z = 5;
camera.position.x = 5;
camera.position.y = 5;
camera.lookAt(0, 1.5, 0);
camera.updateProjectionMatrix();
// var controls = new THREE.OrbitControls( camera );


// Renderer
var renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );


// Model: 
var material = new THREE.MeshStandardMaterial();

var geometry = new THREE.BoxGeometry( 2, 1, 2 );
var base = new THREE.Mesh( geometry, material );
scene.add( base );

var shoulder = new THREE.Object3D();
shoulder.translateY(0.5);
base.add(shoulder);

geometry = new THREE.BoxGeometry(1.0, 1, 1.0);
var lowerArm = new THREE.Mesh( geometry, material );
lowerArm.translateY(0.5);
shoulder.add(lowerArm);

var elbow = new THREE.Object3D();
elbow.translateY(0.5);
lowerArm.add(elbow);

geometry = new THREE.BoxGeometry(0.5, 1, 0.5);
var higherArm = new THREE.Mesh( geometry, material);
higherArm.translateY(0.5);
elbow.add(higherArm);



// Light
var light = new THREE.DirectionalLight(0xffffff, 1.0);
light.position.set(10, 5, 10);
light.target = base;
scene.add(light);

light = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(light);


// Options (DAT.GUI)
var options = {
  base: 0,
  shoulder: 0,
  elbow: 0,
};
// DAT.GUI Related Stuff
var gui = new dat.GUI();
gui.add(options, 'base', -180, 180).listen();
gui.add(options, 'shoulder', -180, 180).listen();
gui.add(options, 'elbow', -180, 180).listen();

// Rendering
var zAxis = new THREE.Vector3(0, 0, 1);
var yAxis = new THREE.Vector3(0, 1, 0);

var render = function () {
  requestAnimationFrame( render );
  
  // Rotate joints
  base.setRotationFromAxisAngle(yAxis, options.base * Math.PI / 180)
  shoulder.setRotationFromAxisAngle(zAxis, options.shoulder * Math.PI / 180);
  elbow.setRotationFromAxisAngle(zAxis, options.elbow * Math.PI / 180);

  // Render
  renderer.render( scene, camera );
};

render();