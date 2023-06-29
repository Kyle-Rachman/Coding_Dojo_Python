// let registration_form = document.getElementById('registration-form');
// registration_form.onsubmit = async function(e){
//     e.preventDefault()
//     let form = new FormData(registration_form)
//     response = await fetch("http://localhost:5000/register", { method :'POST', body : form})
//     data = await response.json()
//     return registration_form.reset()
// }

// let login_form = document.getElementById('login-form');
// login_form.onsubmit = async function(e){
//     e.preventDefault()
//     let form = new FormData(login_form)
//     response = await fetch("http://localhost:5000/login", { method :'POST', body : form})
//     data = await response.json()
//     return login_form.reset()
// }