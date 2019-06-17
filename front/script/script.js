'use strict';
// #region Algemeen
//const IP = prompt('geef publiek IP', 'http://127.0.0.1:5000');
//const IP = window.location.hostname + 'http://169.254.10.1:5000';
let socket;
let deur;
let gordijn;
let graden;
let vocht;
console.log('test');
let lanIP = '169.254.10.1';
const listenToButton = function() {
  deur.addEventListener('click', function() {
    console.log('click op de drukknop');
    socket.emit('button');
  });
};

const listenToKnop = function() {
  gordijn.addEventListener('click', function() {
    console.log('click op de drukknop');
    socket.emit('knop');
  });
};

const getSocketConnection = function() {
  socket = io(`http://${lanIP}:5000`);

  socket.on('giveTemp', function(data) {
    console.log(data);
    console.log(graden);
    graden.innerText = (data + "°c");
  });
//
  socket.on('giveVocht', function(data) {
    console.log(data);
    console.log(vocht);
    vocht.innerText = (data + "%");
  });
};

const livedata = function() {
  socket.emit('getTemp');
  socket.emit('getVocht');

};

const init = function() {
  deur = document.querySelector('#deur');
  getSocketConnection();

  listenToButton();
  gordijn = document.querySelector('#gordijnen');

  listenToKnop();
  graden = document.querySelector('#temp');
  vocht = document.querySelector('#vocht');
  livedata();
};

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  console.log('test');
  init();
});

// #endregion
