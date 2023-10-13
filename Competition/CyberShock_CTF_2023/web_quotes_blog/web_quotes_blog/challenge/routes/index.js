const bot            = require('../bot');
const express        = require('express');
const router         = express.Router();
const JWTHelper      = require('../helpers/JWTHelper');
const AuthMiddleware = require('../middleware/AuthMiddleware');

let db;
let botVisting = false;
const response = data => ({ message: data });

router.get('/', (req, res) => {
	return res.render('index.html');
});

router.post('/api/register', async (req, res) => {
	const { username, password } = req.body;

	if (username && password) {
		return db.checkUser(username)
			.then(user => {
				if (user) return res.status(401).send(response('User already registered!'));
				return db.registerUser(username, password)
					.then(()  => res.send(response('User registered successfully!')))
			})
			.catch(() => res.send(response('Something went wrong!')));
	}
	return res.status(401).send(response('Please fill out all the required fields!'));
});

router.post('/api/login', async (req, res) => {
	const { username, password } = req.body;

	if (username && password) {
		return db.loginUser(username, password)
			.then(user => {
				let token = JWTHelper.sign({ username: user.username });
				res.cookie('session', token, { maxAge: 3600000 });
				return res.send(response('User authenticated successfully!'));
			})
			.catch(() => res.status(403).send(response('Invalid username or password!')));
	}
	return res.status(500).send(response('Missing parameters!'));
});

router.get('/feed', AuthMiddleware, async (req, res) => {
	return db.getPosts()
		.then(feed => {
			res.render('feed.html', { feed, user: req.data });
		})
		.catch(() => res.status(500).send(response('Something went wrong, please try again!')));
});

router.get('/submissions', AuthMiddleware, async (req, res, next) => {
	return db.getUserPosts(req.data.username)
		.then(posts => {
			res.render('submissions.html', { user: req.data, posts });
		})
		.catch(() => res.status(500).send(response('Something went wrong, please try again!')));

});

router.get('/review', async (req, res) => {
	if(req.ip != '127.0.0.1') return res.redirect('/');

	return db.getPosts(0)
		.then(feed => {
			res.render('review.html', { feed });
		})
		.catch(() => res.status(500).send(response('Something went wrong, please try again!')));
});

router.post('/api/submit', AuthMiddleware, async (req, res) => {
	const { content } = req.body;
	if(content){
		try {
			await db.addPost(req.data.username, content);
			botVisting = true;
			await bot.reviewPost();
			await db.archiveSubmittedPosts();
			botVisting = false;
			return res.send(response('Your submission is being reviewed by an admin!'));
		}
		catch(e) {
			console.log(e);
			botVisting = false;
			return res.send(response('Something went wrong, please try again!'));
		}
	}
	return res.status(403).send(response('Please write your quote first!'));
});

router.get('/logout', (req, res) => {
	res.clearCookie('session');
	return res.redirect('/');
});

module.exports = database => {
	db = database;
	return router;
};