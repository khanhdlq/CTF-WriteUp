function checkName(name){

    var check  = name.split("").reverse().join("");
    if (check === "uyjnimda")
    //adminjyu
        return true;
    else
        return false;
}

function checkLength(pwd){
    if (password.length % 6 === 0 )
        return true;
    else
        return false;
}
function checkValidity(password){
    const arr = Array.from(password).map(ok);
    function ok(e){
        if (e.charCodeAt(0)<= 'z' && e.charCodeAt(0) >= 'a'){
        return e.charCodeAt(0);
    }}

    let sum = 0;
    for (let i = 0; i < arr.length; i+=6){
        var add = arr[i] & arr[i + 2]; 
        var or = arr[i + 1] | arr[i + 4]; 
        var xor = arr[i + 3] ^ arr[i + 5];
        if (add === 0x60   && or === 0x61   && xor === 0x6) 
            sum += add + or - xor; 
    }
    if (sum === 0xbb)
        return true;
    else
        return false;
}
// /check.php 
var btn = document.getElementsByClassName('btn-1')[0];
btn.addEventListener('click',(e)=>{
    e.preventDefault();

    var nam = document.getElementById('name').value;
    if(!(checkName(nam))){         
         alert('Incorrect Name! 😥😥')
    }
    else{
           alert('Correct Name! 🙂🙂')
    }

    var pwd = document.getElementById('password').value;
    if(!checkValidity(pwd) && !checkLength(pwd)){
            alert('Incorrect Password! 😥😥')
    }
    else{
           alert('Correct Password! 🙂🙂')
    }
});
