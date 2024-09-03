const express = require("express");
const path = require("path");
const http = require("http");
const fs = require("fs");

require("dotenv").config();

const app = express();

// Serve static files from the "client" directory
app.use(express.static(path.join(__dirname)));

// Serve the index.html file
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// Serve the prognosis.js file
app.get("/prognosis.js", (req, res) => {
  res.sendFile(path.join(__dirname, "prognosis.js"));
});

// Handle GET requests to /prognosis
app.get("/prognosis", (req, res) => {
  const { month, day } = req.query;

  // Here you can process the month and day parameters and generate a response
  const response = {
    message: `The prognosis for ${month}/${day} is looking good!`
  };

  res.json(response);
});

// Catch-all route to handle any other requests
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "client", "index.html"));
});

const httpServer = http.createServer(app);

const PORT = process.env.WEBSERVER_PORT || 8000;
const IP = process.env.IP || "localhost";
httpServer.listen(PORT, () => {
  console.log(`Server on http://${IP}:${PORT}`);
});

module.exports = { app, httpServer };
