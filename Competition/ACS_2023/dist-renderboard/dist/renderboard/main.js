const express = require('express')
const session = require('express-session')
const bodyParser = require('body-parser');
const FileStore = require('session-file-store')(session)
const path = require('path')
const multer = require('multer');
const sanitizeHtml = require('sanitize-html');
const mysql = require('mysql');

var authRouter = require('./auth');
var authCheck = require('./authCheck.js');
var template = require('./template.js');
var db = require('./db');

const app = express()
const port = 22223

//Settings ejs
app.set('views', path.join(__dirname, '/public/html'));
app.set('view engine', 'ejs');

app.disable('x-powered-by')
app.use(express.static(path.join(__dirname, 'public')))
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
  secret: 'test',
  resave: false,
  saveUninitialized: true,
  store:new FileStore({ path: './sessions' }),
}))

app.get('/', (req, res) => {
  if (!authCheck.isOwner(req, res)) {  
    res.redirect('/auth/login');
    return false;
  } else {                                      
    res.redirect('/main');
    return false;
  }
})

app.use('/auth', authRouter);
app.use(bodyParser.json());
app.use(express.json());

app.get('/main/admin_notice', (req, res) => {
  if (!authCheck.isOwner(req, res)) { 
    res.redirect('/auth/login');
    return;
  }

  if (req.session.is_admin === 1) {
    const page = parseInt(req.query.page || '1', 10);
    const postsPerPage = 10;
    const countQuery = 'SELECT COUNT(*) AS total FROM admin_notice';

    const query = `
      SELECT * FROM admin_notice
      ORDER BY no DESC
      LIMIT ?
      OFFSET ?
    `;

    db.query(countQuery, (err, countResults) => {
      if (err) {
        console.error('Error fetching total posts', err);
        return res.status(500).send('Internal Server Error');
      }
      
      const totalPosts = countResults[0].total;
      const totalPage = Math.ceil(totalPosts / postsPerPage);

      db.query(query, [postsPerPage, (page - 1) * postsPerPage], (err, results) => {
        if (err) {
          console.error('Error fetching paged posts', err);
          return res.status(500).send('Internal Server Error');
        }

      const data = {
        boards: results,
        currentPage: page,
        totalPage: totalPage,
        authCheck: {
          statusUI: authCheck.statusUI(req, res)
        }
      };
      res.render('admin_board', data);
      })
    });
  }
  else {
    res.send(`<script type="text/javascript">alert("Access Denied"); 
    document.location.href="/main";</script>`);
  }
  
});

app.get('/main/admin_notice/write', (req, res) => {
  const isAdmin = req.session.is_admin === 1;

  if(isAdmin){
    res.render('admin_write');
  } else {
    res.send(`<script type="text/javascript">alert("Access Denied"); 
    document.location.href="/main";</script>`);
  }
})

app.post('/main/admin_notice/write', (req, res) => {
  const title = req.body.title;
  const content = req.body.content;
  const author = req.session.nickname;

  const query = `INSERT INTO admin_notice(title, content, author) VALUES (?, ?, ?)`
  console.log(query)

  db.query(query,[title,content, author], (err, result) => {
    if (err) {
      console.error('Error', err);
      res.status(500).send('Internal Server Error');
    } else {
      console.log("notice Success");
      res.redirect('/main/admin_notice');
    }
  });
});

app.get('/main/admin_notice/detail', (req, res) => {
  const postNo = req.query.no;
  console.log(req.query)
  const query = `
    SELECT * FROM admin_notice WHERE no = ?
  `;
  console.log(query)
  db.query(query, [postNo], (err, result) => {
    if (err) {
      console.error('Error fetching post details', err);
      return res.status(500).send('Internal Server Error');
    }

    if (result.length === 0) {
      return res.status(404).send('Post not found');
    }

    const isAdmin = req.session.is_admin === 1;

    if (!isAdmin) {
      return res.send(`<script type="text/javascript">alert("Access Denied. You are not admin."); 
      document.location.href="/main/admin_notice";</script>`);
    }
    console.log("[+]result ", result);
    res.render('admin_board_detail', { ...req.query, post: result[0], isAdmin });
  });
});

app.get('/main/board', (req, res) => {
  if (!authCheck.isOwner(req, res)) {
    res.redirect('/auth/login');
    return;
  }

  const page = parseInt(req.query.page || '1', 10);  
  const postsPerPage = 10; 

  const countQuery = 'SELECT COUNT(*) AS total FROM boards';

  const query = `
    SELECT * FROM boards
    ORDER BY no DESC
    LIMIT ?
    OFFSET ?
  `;
  db.query(countQuery, (err, countResults) => {
    if (err) {
      console.error('Error fetching total posts', err);
      return res.status(500).send('Internal Server Error');
    }
    
    const totalPosts = countResults[0].total;
    const totalPage = Math.ceil(totalPosts / postsPerPage);

    db.query(query, [postsPerPage, (page - 1) * postsPerPage], (err, results) => {
      if (err) {
        console.error('Error fetching paged posts', err);
        return res.status(500).send('Internal Server Error');
      }

    const data = {
      boards: results,
      currentPage: page,
      totalPage: totalPage,
      authCheck: {
        statusUI: authCheck.statusUI(req, res)
      }
    };
  
    res.render('board', data);
    })
  });
});

app.get('/main/board/write', (req, res) => {
  res.render('write')
})

app.post('/main/board/write', (req, res) => {
  const title = req.body.title;
  const content = req.body.content;
  const query = `INSERT INTO boards(title, content) VALUES (?, ?)`
  console.log(query)

  db.query(query,[title,content], (err, result) => {
    if (err) {
      console.error('Error', err);
      res.status(500).send('Internal Server Error');
    } else {
      console.log("board write Success");
      res.redirect('/main/board');
    }
  });
});

app.get('/main/board/detail', (req, res) => {
  const postNo = req.query.no;
  console.log(req.query)
  const query = `SELECT * FROM boards WHERE no = ?`;
  console.log(query)
  db.query(query, [postNo], (err, result) => {
    if (err) {
      console.error('Error fetching post details', err);
      return res.status(500).send('Internal Server Error');
    }

    if (result.length === 0) {
      return res.status(404).send('Post not found');
    }

    const post = result[0];
    if (req.session.is_admin === 1) {
      return res.send(`<script type="text/javascript">alert("Access Denied. You are not admin."); 
      document.location.href="/main/board";</script>`);
    }
    console.log("[+]result ",result)
    res.render('board_detail', { post: result[0] });
  });
});

app.get('/main/notice', (req, res) => {
  //user info search
  const query = `select is_admin from user where redacted1 = ?`;
  db.query(query, [req.session.nickname], (error, results) => {
    if(error) {
      console.error(error);
      res.status(500).send("Internal Server Error");
      return ;
    }
  
    const isAdmin = results[0] && results[0].is_admin === 1;
    if(isAdmin) {
      res.render('notice');
    }
    else {
      res.send(`<script type="text/javascript">alert("[!] Access Denied");
      document.location.href="/main";</script>`)
    }
  })
})

app.post('/main/notice', (req, res) => {
  const index1 = req.body.title;
  const contents = req.body.content;
  const author = req.session.nickname;
  console.log(index1)
  console.log(contents)
  
  const insert_query = `INSERT INTO boards(title, content, author) VALUES (?, ?, ?)`;

  db.query(insert_query, [index1, contents, author], (err, result) => {
    if (err) {
      console.error('Error', err);
    } else {
      console.log("Notice Success");
      res.redirect('/main');
    }
  })
})
 
app.get('/main', (req, res) => {
  if (!authCheck.isOwner(req, res)) {  
    res.redirect('/auth/login');
    return;
  }

  const query = `select is_admin from user where redacted1 = ?`;
  db.query(query, [req.session.nickname], (error, results) => {
    if (error) {
      console.error(error);
      res.status(500).send("Internal Server Error");
      return;
    }

    const isLogin = results[0] && results[0].is_admin === 1;
    const data = {
      authCheck: {
        statusUI: authCheck.statusUI(req, res)
      },
      isLogin  
    };
    
    res.render('main', data);
  });
});

app.get('/auth/logout', (req, res) => {
  req.session.destroy(function(err) {
      res.redirect('/');
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})