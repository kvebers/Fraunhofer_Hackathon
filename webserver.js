const express = require("express");
const path = require("path");
const http = require("http");
const { execFile } = require("child_process");
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
  const scriptPath = path.join(__dirname, "predict.py");

  // Call the Python script
  execFile("python3", [scriptPath, month, day], (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error}`);
      return res.status(500).json({ error: "Internal Server Error" });
    }

    if (stderr) {
      console.error(`Script stderr: ${stderr}`);
      return res.status(500).json({ error: "Internal Server Error" });
    }

    // Parse the JSON output from the Python script
    try {
      const output = JSON.parse(stdout);
      res.json(output);
    } catch (parseError) {
      console.error(`Error parsing JSON: ${parseError}`);
      res.status(500).json({ error: "Internal Server Error" });
    }
  });
});

const httpServer = http.createServer(app);

const PORT = process.env.WEBSERVER_PORT || 8000;
const IP = process.env.IP || "localhost";
httpServer.listen(PORT, () => {
  console.log(`Server on http://${IP}:${PORT}`);
});

module.exports = { app, httpServer };
