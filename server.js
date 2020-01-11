var port = '8080';

var bodyParser = require('body-parser'); 
var jsonParser = bodyParser.json();
var cors = require("cors"); 
var logger = require('morgan');

var express = require('express'); 
var app = express(); 

app.use(logger);
app.use(cors()); 
app.use(bodyParser.json()); 
var server = app.listen(8080, "0.0.0.0");

app.use("/", express.static("./client/"));

app.get('/kappa', function(req, res) {
    console.log('oiajdoiasjd');
    res.send('owo');
});

app.get('/featuredBooks', function(req, res) {
    books.getFeaturedBooks(req, res, con,app.get('jwtTokenSecret'));
});