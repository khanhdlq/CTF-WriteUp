const puppeteer = require('puppeteer');

const browser_options = {
	headless: true,
	args: [
		'--no-sandbox',
		'--disable-background-networking',
		'--disable-default-apps',
		'--disable-extensions',
		'--disable-gpu',
		'--disable-sync',
		'--disable-translate',
		'--hide-scrollbars',
		'--metrics-recording-only',
		'--mute-audio',
		'--no-first-run',
		'--safebrowsing-disable-auto-update',
		'--js-flags=--noexpose_wasm,--jitless'
	]
};

const reviewPost = async () => {
    try {
		const browser = await puppeteer.launch(browser_options);
		let context = await browser.createIncognitoBrowserContext();
		let page = await context.newPage();
		await page.setCookie({
			name: "flag",
			'value': 'HTB{f4k3_fl4g_f0r_t3st1ng}',
			domain: "127.0.0.1:1337"
		});
		await page.goto('http://127.0.0.1:1337/review', {
			waitUntil: 'networkidle2',
			timeout: 5000
		});
		await browser.close();
    } catch(e) {
        console.log(e);
    }
};

module.exports = { reviewPost };