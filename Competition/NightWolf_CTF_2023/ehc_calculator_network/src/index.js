const crypto = require('crypto');
const express = require('express');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const { NodeVM } = require('vm2');
const pathval = require('pathval');
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

const vm = new NodeVM({
  eval: false,
  wasm: false,
  wrapper: 'none',
  strict: true
});

const prime_hash_code = ["efae8c473769eec5f6af45a1f76c87d2f769e92d", "a92aa0a40cc0b7f0d87c4c767717a8d29e6a619c"];

const ripemd160WithRSA = (data) => crypto.createHash('ripemd160WithRSA').update(data).digest('hex');

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use("/", express.static(__dirname + "/static"));
app.use(cookieParser());

app.post('/calc', (req, res, next) => {
    let calc = req.body.calc ?? '';
    let result;
    try {
        result = vm.run(`return ${calc}`);
    }
    catch(err) {
        console.log(err);
        return res.send("Error");
    }

    if(typeof result !== "number") {
        return res.send("Format");
    }

    res.send("Result: "+result);
});


app.get('/hidden', (req, res, next) => {
  try{
    res.sendFile(__dirname + "/static/hidden.html");
  } catch (error){
    res.send(error);
  }
});

app.post('/hidden', (req, res, next) => {
  try{
    let code = req.body.code ?? '';
    let hash = ripemd160WithRSA(code);
    console.log(prime_hash_code.filter(p => p === hash)[0] === '')
    if(prime_hash_code.filter(p => p === hash)[0] !== undefined) {
      const prime_token = jwt.sign({isPrime: true}, process.env.JWT_SECRET_KEY);
      res.cookie('prime', prime_token);
      res.send('prime');
    }
    else res.send('Non-prime');
    return;
  } catch (error){
    res.send(error);
  }
});

const combine = (sink, source) => {
  for (var property in source) {
      if (typeof sink[property] === 'object' && typeof source[property] === 'object') {    
          combine(sink[property], source[property]);
      } else {
          sink[property] = source[property];
      }
  }
  return sink
};

app.get('/prime', (req, res) => {
  try {
    const prime_token = req.cookies['prime'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY)){
      res.sendFile(__dirname + "/static/prime.html");
    } else{
      return res.status(401).send(error);
    }
  } catch (error) {
    return res.status(401).send(error);
  }
});

app.post('/quote1', function (req, res, next) {
  try {
    const prime_token = req.cookies['prime'];
    console.log(jwt.verify(prime_token, process.env.JWT_SECRET_KEY))
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY).isPrime){
      console.log("in quote 1")
      const Quote = req.body.list.toString();
      const getQuote = require("./static/" + Quote);
      res.json(getQuote.all());
    } else{
      return res.status(401).send(error);
    }
  } catch (error) {
    return res.status(401).send(error);
  }
})

app.post('/quote2', function (req, res, next) {
  try {
    const prime_token = req.cookies['prime'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY)){
      const Quote1 = require("./static/top-quote-1.js")
      const Quote2 = require("./static/top-quote-2.js")
      let superQuote = combine(Quote1.all(), Quote2.all())
      if (req.body.add){
        let content = req.body.content || "co cai loz dcbcm";
        let name = req.body.name || "antoinenguyen_09";
        superQuote = pathval.set(superQuote, name, content);
      }
      res.json(superQuote);
    } else{
      return res.status(401).send(error);
    }
  } catch (error) {
    return res.status(401).send(error);
  }
})

app.listen(3000, () => {
  console.log('listening on port 3000');
});