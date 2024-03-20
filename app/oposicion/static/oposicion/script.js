
const eye1 = document.getElementById('eye1');
const password1 = document.getElementById('password1');
const eye2 = document.getElementById('eye2');
const password2 = document.getElementById('password2');


eye1.addEventListener('click', mostrarContraseña1);

function mostrarContraseña1(){
    if(password1.type == "password"){
        password1.type = "text";
        eye1.src = "/static/usuarios/img/eyeopen.png"
    } else {
        password1.type = "password";
        eye1.src = "/static/usuarios/img/eyeclose.png";
    }
}

eye2.addEventListener('click', mostrarContraseña2);

function mostrarContraseña2(){
    if(password2.type == "password"){
        password2.type = "text";
        eye2.src = "/static/usuarios/img/eyeopen.png"
    } else {
        password2.type = "password";
        eye2.src = "/static/usuarios/img/eyeclose.png";
    }
}
