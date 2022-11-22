const express = require('express');
const morgan = require('morgan');

let port = 3000;
let host = 'localhost';

app.listen(port, host, ()=>{
    console.log('Server is running on port', port);
});