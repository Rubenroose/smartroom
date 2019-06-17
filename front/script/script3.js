'use strict';
// #region Algemeen
//const IP = prompt('geef publiek IP', 'http://127.0.0.1:5000');
//const IP = window.location.hostname + 'http://169.254.10.1:5000';
let socket;
let procent;

console.log('test');
let lanIP = '169.254.10.1';

const getSocketConnection = function() {
  socket = io(`http://${lanIP}:5000`);

  socket.on('giveProcent', function(data) {
    console.log(data);
    console.log(procent);
    procent.innerText = data + '°c';
  });
};

const livedata = function() {
  socket.emit('getProcent');
};

const init = function() {
  getSocketConnection();
  procent = document.querySelector('#vo');
  livedata();
};

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  console.log('test');
  init();
});

// #endregion
