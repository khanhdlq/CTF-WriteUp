const fs = require('node:fs');
const path = require('path')

/*
I wonder what is inside /next.txt  
*/

const secret = '39c8e9953fe8ea40ff1c59876e0e2f28'
const server = Bun.serve({
  port: 8000,
  fetch(req) {
  	let url = new URL(req.url);
  	let pname = url.pathname;
  	if(pname.startsWith(`/${secret}`)){
      if(pname.startsWith(`/${secret}/read`)){
        try{
          let fpath = url.searchParams.get('file');
          if(path.basename(fpath).indexOf('next') == -1){ 
            return new Response(fs.readFileSync(fpath).toString('base64'));
          } else {
            return new Response('no way');
          }
        } catch(e){ }
        return new Response("Couldn't read your file :(");
      }
      return new Response(`did you know i can read files?? amazing right,,, maybe try /${secret}/read/?file=/proc/self/cmdline`);
    }
    return 
  }
});