var mysql = require('mysql');
var db = mysql.createConnection({
    host: 'db',
    user: 'root',
    password: '1324',
    database: 'acs_data'
});
db.connect();

module.exports = db;