const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const formregister = document.getElementById('formregister');
const formlogin = document.getElementById('formlogin');

const eye = document.getElementById('eye');
const password = document.getElementById('password');
const eye1 = document.getElementById('eye1');
const password1 = document.getElementById('password1');
const eye2 = document.getElementById('eye2');
const password2 = document.getElementById('password2');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
    formlogin.reset();
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
    formregister.reset();
});

eye.addEventListener('click', mostrarContraseña);

function mostrarContraseña(){
    if(password.type == "password"){
        password.type = "text";
        eye.src = "/static/usuarios/img/eyeopen.png"
    } else {
        password.type = "password";
        eye.src = "/static/usuarios/img/eyeclose.png";
    }
}

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
