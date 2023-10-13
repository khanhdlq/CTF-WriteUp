const sqlite = require('sqlite-async');

class Database {
	constructor(db_file) {
		this.db_file = db_file;
		this.db = undefined;
	}

	async connect() {
		this.db = await sqlite.open(this.db_file);
	}

	async migrate() {
		return this.db.exec(`
            DROP TABLE IF EXISTS users;

            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                password   VARCHAR(255) NOT NULL,
                avatar     VARCHAR(255) NOT NULL
            );

            DROP TABLE IF EXISTS posts;

            CREATE TABLE IF NOT EXISTS posts (
                id         INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
                author  VARCHAR(255) NOT NULL,
                content    VARCHAR(255) NOT NULL,
                approved   INTEGER      NOT NULL,
                created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
            );

            INSERT INTO posts (author, approved, content) VALUES ('Haemin', 1, 'It is a sign of great spiritual strength to keep someone else’s secret.');
            INSERT INTO posts (author, approved, content) VALUES ('Mark', 1, 'Don’t just sit there. Do something. The answers will follow.');
			INSERT INTO posts (author, approved, content) VALUES ('Haemin', 1, 'You are beautiful not because you are better than others, but because there is only you who can smile like that.');
			INSERT INTO posts (author, approved, content) VALUES ('Austin', 1, 'Steal like an artist.');
            INSERT INTO posts (author, approved, content) VALUES ('Oscar', 1, 'Be yourself; everyone else is already taken.');
        `);
	}

	async registerUser(user, pass) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('INSERT INTO users (username, password, avatar) VALUES ( ?, ?, "default.jpg")');
				resolve((await stmt.run(user, pass)));
			} catch(e) {
				reject(e);
			}
		});
	}

	async loginUser(user, pass) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT username FROM users WHERE username = ? and password = ?');
				resolve(await stmt.get(user, pass));
			} catch(e) {
				reject(e);
			}
		});
	}

	async getUser(user) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT * FROM users WHERE username = ?');
				resolve(await stmt.get(user));
			} catch(e) {
				reject(e);
			}
		});
	}

	async checkUser(user) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT username FROM users WHERE username = ?');
				let row = await stmt.get(user);
				resolve(row !== undefined);
			} catch(e) {
				reject(e);
			}
		});
	}

	async addPost(author, content) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('INSERT INTO posts (author, content, approved) VALUES (? , ?, 0)');
				resolve(await stmt.run(author, content));
			} catch(e) {
				reject(e);
			}
		});
	}

	async archiveSubmittedPosts() {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('UPDATE posts SET approved = 2 WHERE approved = 0');
				resolve(await stmt.run());
			} catch(e) {
				reject(e);
			}
		});
	}

	async getPosts(approved=1) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT * FROM posts WHERE approved = ?');
				resolve(await stmt.all(approved));
			} catch(e) {
				reject(e);
			}
		});
	}

	async getUserPosts(username) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT * FROM posts WHERE author = ?');
				resolve(await stmt.all(username));
			} catch(e) {
				reject(e);
			}
		});
	}

}

module.exports = Database;