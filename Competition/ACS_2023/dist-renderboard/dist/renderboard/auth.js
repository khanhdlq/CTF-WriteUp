var express = require('express');
var router = express.Router();
var path = require('path')
var template = require('./template.js');
var db = require('./db');
var bodyParser = require('body-parser');

router.use(bodyParser.json());
router.use(bodyParser.urlencoded({extended : false}));
router.get('/login', function (request, response) {
    response.render('login')
});

router.post('/login_process', function (request, response) {
    var id = request.body.username;
    var pw = request.body.pwd;
    if (id && pw) {
        db.query('SELECT * FROM user WHERE redacted1 = ? AND redacted2 = ?', [id, pw], function(error, results, fields) {
            if (error) throw error;
            if (results.length > 0) {
                request.session.is_logined = true; 
                request.session.nickname = id;
                var is_admin = results[0].is_admin;
                request.session.is_admin = is_admin;
                request.session.save(function () {
                    response.redirect(`/`);
                });
            } else {              
                response.send(`<script type="text/javascript">alert("Not Match ID/PW"); 
                document.location.href="/auth/login";</script>`);    
            }            
        });

    } else {
        response.send(`<script type="text/javascript">alert("Input ID/PW"); 
        document.location.href="/auth/login";</script>`);    
    }
});

router.get('/logout', function (request, response) {
    request.session.destroy(function (err) {
        response.redirect('/');
    });
});

router.get('/register', function(request, response) {
    response.render('register')
});

router.post('/check_duplicate', function (request, response) {
    try{
        const id1 = request.body.username;
        console.log("[!] Received id:", id1);

        if (id1.match(/'|_|or| |and|%20|\.|\(|\)/i)) {
            response.status(400).json({ error: 'Invalid input' });
            return;
        }
        const id2 = id1.replace(new RegExp('substr|mid|like|char|hex|ord', 'gi'), '');
        console.log("[!] Replace :", id2)

        const id = decodeURIComponent(id2);
        console.log("[!] URI Decode ID : ", id)

        const query = `SELECT * FROM user WHERE redacted1 = '${id}'`;
        db.query(query, function (error, results, fields) {
            console.log(results)
            if (error) {
                console.error(error);
                const use_id = id;
                response.status(500).json({ error: 'Internal server error' , Syntax_Error :use_id});
            } else {
                if (results.length === 0) {
                    
                    response.json({ available: true });
                } else {
                    const use_id = id;
                    response.json({ available: false , searchid: use_id});
                }
            }
        });
    }
    catch (error) {
        console.error(error);
        response.status(500).json({error : 'Internal Server Error'});
    }
});

router.post('/register_process', function(request, response) {    
    var id = request.body.username;
    var pw = request.body.pwd;    
    var pw2 = request.body.pwd2; 
    var email = request.body.email;

    if (id && pw && pw2 && email) {
        if(id.length > 30) {
            response.send(`
                <script type="text/javascript">
                    alert("ID Length Limit 30");
                    document.location.href="/auth/register";
                </script>
            `);
            return;
        }
        if (pw.length > 50) {
            response.send(`
                <script type="text/javascript">
                    alert("Password Length Limit 50");
                    document.location.href="/auth/register";
                </script>
            `);
            return;
        }
        if (email.length > 50) {
            response.send(`
                <script type="text/javascript">
                    alert("email Length Limit 50");
                    document.location.href="/auth/register";
                </script>
            `);
            return;
        }

        db.query('SELECT * FROM user WHERE redacted1 = ?', [id], function(error, idResults, fields) {
            if (error) throw error;

            db.query('SELECT * FROM user WHERE redacted3 = ?', [email], function(error, emailResults, fields) {
                if (error) throw error;

                if (idResults.length <= 0 && emailResults.length <= 0 && pw == pw2) {
                    db.query('INSERT INTO user (redacted1, redacted2, redacted3) VALUES(?,?,?)', [id, pw, email], function (error, data) {
                        if (error) throw error;
                        response.send(`
                            <script type="text/javascript">
                                alert("Regist is Complete !");
                                document.location.href="/";
                            </script>
                        `);
                    });
                } else if (pw != pw2) {
                    response.send(`
                        <script type="text/javascript">
                            alert("Password Entered is Different");
                            document.location.href="/auth/register";
                        </script>
                    `);
                } else if (idResults.length > 0) {
                    response.send(`
                        <script type="text/javascript">
                            alert("ID already exists");
                            document.location.href="/auth/register";
                        </script>
                    `);
                } else if (emailResults.length > 0) {
                    response.send(`
                        <script type="text/javascript">
                            alert("Email already exists");
                            document.location.href="/auth/register";
                        </script>
                    `);
                }
            });
        });
    } else {
        response.send(`
            <script type="text/javascript">
                alert("Information that has not been entered");
                document.location.href="/auth/register";
            </script>
        `);
    }
});

router.get('/findid', function (request, response) {
    response.render('findid')
});
router.post('/findid_process', function (request, response) {
    try {
        const email = request.body.email_id;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            response.status(400).json({ error: 'This is not a valid email format' });
            return;
        }
        console.log("[!] Find email : ", email)

        const query = "SELECT redacted1 FROM user WHERE redacted3 = ?";
        db.query(query, [email], function(error, results, fields) {
            if (results.length > 0) {
                const foundId = results[0].redacted1;
                console.log(`Found ID for email ${email}: ${foundId}`);
                response.json({ id: foundId });
            } else {
                console.log(`No matching ID found for email ${email}`);
                response.json({ error: 'No ID is registered in this email' });
            }
        });
    } catch (error) {
        console.error("Unhandled error:", error);
        response.status(500).json({ error: 'Server Error' });
    }
});

module.exports = router;