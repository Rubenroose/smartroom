'use strict';
// #region Algemeen
//const IP = prompt('geef publiek IP', 'http://127.0.0.1:5000');
//const IP = window.location.hostname + 'http://169.254.10.1:5000';
let socket;
let temp;

console.log('test');
let lanIP = '169.254.10.1';

const getSocketConnection = function() {
  socket = io(`http://${lanIP}:5000`);

  socket.on('giveGraad', function(data) {
    console.log(data);
    console.log(temp);
    temp.innerText = data + '°c';
  });
};

const livedata = function() {
  socket.emit('getGraad');
};

const init = function() {
  getSocketConnection();
  temp = document.querySelector('#graden');
  livedata();
};


document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  console.log('test');
  init();
});

// #endregion
