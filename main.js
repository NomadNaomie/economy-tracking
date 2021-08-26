const fs = require("fs");
const express = require("express");
const app = express();
app.use(express.json());
const http = require("http");
const path = require("path");

app.use("/assets",express.static(path.join(__dirname, "/assets")));
app.get('/favicon.ico', express.static('favicon.ico'));
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'assets/html/HermitCraftEconomy.html'));
});
http.createServer(app).listen(9040);