async function get_users(){
    let response = await fetch('http://localhost:5000/users')
    let data = await response.json()
    let users = document.getElementById('users');
        for( let i = 0; i < data.length; i++){
            let row = document.createElement('tr');

            let name = document.createElement('td');
            name.innerHTML = data[i].user_name;
            row.appendChild(name);
            
            let email = document.createElement('td');
            email.innerHTML = data[i].email;
            row.appendChild(email);
            users.appendChild(row);
        }
    return data
}

async function get_new_user(){
    let response = await fetch('http://localhost:5000/users')
    let data = await response.json()
    let users = document.getElementById('users');
    let row = document.createElement('tr');
    let name = document.createElement('td');
    name.innerHTML = data[data.length-1].user_name;
    row.appendChild(name);
    let email = document.createElement('td');
    email.innerHTML = data[data.length-1].email;
    row.appendChild(email);
    users.appendChild(row);
    return data
}

get_users();

let myForm = document.getElementById('new_user_form');
myForm.onsubmit = async function(e){
    e.preventDefault()
    let form = new FormData(myForm)
    response = await fetch("http://localhost:5000/create/user", { method :'POST', body : form})
    data = await response.json()
    get_new_user()
    return myForm.reset()
}

