import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';
import App from './client/App';
import Html from './client/Html';
import { ServerStyleSheet } from 'styled-components'; // <-- importing ServerStyleSheet

const port = 3000;
const client_port = 8000;
const server = express();

const io = require('socket.io')();

// Creating a single index route to server our React application from.
server.get('/', (req, res) => {
  const sheet = new ServerStyleSheet(); // <-- creating out stylesheet

  io.on('connection', (client) => {
    client.on('subscribeToTimer', (interval) => {
      console.log('client is subscribing to timer with interval ', interval);
      setInterval(() => {
        client.emit('timer', new Date());
      }, interval);
    });
  });
  io.listen(client_port);
  console.log(`listening on port:${client_port}`);

  const body = renderToString(sheet.collectStyles(<App />)); // <-- collecting styles
  const styles = sheet.getStyleTags(); // <-- getting all the tags from the sheet
  const title = 'Project 2 Frontend';

  res.send(
    Html({
      body,
      styles, // <-- passing the styles to our Html template
      title
    })
  );
});

server.listen(port);
console.log(`Serving at http://localhost:${port}`);