if (window.location.href == 'http://localhost:5000/') {
    let registration_form = document.getElementById('registration-form');
    registration_form.onsubmit = async function(e){
        e.preventDefault()
        let form = new FormData(registration_form)
        response = await fetch("http://localhost:5000/register", { method :'POST', body : form})
        data = await response.json()
        if(data["message"]){
            location.href = '/recipes'
        }
        else{
            all_flashes = $(".errors")
            all_flashes.each(function(){
                $(this).html("")
            })
            errors = $("#registration-errors")
            for(let i=0; i < data.length; i++){
                errors.append(`<p>${data[i]}</p>`)
            }
        }
        registration_form.reset()
    }

    let login_form = document.getElementById('login-form');
    login_form.onsubmit = async function(e){
        e.preventDefault()
        let form = new FormData(login_form)
        response = await fetch("http://localhost:5000/login", { method :'POST', body : form})
        data = await response.json()
        if(data["message"]){
            location.href = '/recipes'
        }
        else{
            all_flashes = $(".errors")
            all_flashes.each(function(){
                $(this).html("")
            })
            errors = $("#login-errors")
            for(let i=0; i < data.length; i++){
                errors.append(`<p>${data[i]}</p>`)
            }
        }
        login_form.reset()
    }
}

else if (window.location.href == 'http://localhost:5000/recipes') {
    get_recipes()
    let recipe_form = document.getElementById('create-recipe-form');
    recipe_form.onsubmit = async function(e){
        e.preventDefault()
        let form = new FormData(recipe_form)
        response = await fetch("http://localhost:5000/recipes/create", { method :'POST', body : form})
        data = await response.json()
        if(data["message"]){
            get_new_recipe()
        }
        else{
            errors = $("#recipe-errors")
            errors.html("")
            for(let i=0; i < data.length; i++){
                errors.append(`<p>${data[i]}</p>`)
            }
        }
        recipe_form.reset()
    }
}

else if (document.URL.match(/^http:\/\/localhost\:5000\/recipes\/\d+/)) {
    let recipe_form = document.getElementById('edit-recipe-form');
    recipe_form.onsubmit = async function(e){
        e.preventDefault()
        let form = new FormData(recipe_form)
        response = await fetch("http://localhost:5000/recipes/edit", { method :'POST', body : form})
        data = await response.json()
        if(data["message"]){
            update_recipe()
        }
        else{
            errors = $("#recipe-errors")
            errors.html("")
            for(let i=0; i < data.length; i++){
                errors.append(`<p>${data[i]}</p>`)
            }
        }
        recipe_form.reset()
    }
}

async function get_recipes() {
    let response = await fetch('http://localhost:5000/read/recipes')
    let data = await response.json()
    let recipes = document.getElementById('recipes-table-body');
    let session_user_id = document.getElementById('users_id').value
        for( let i = 0; i < data.length; i++){
            let row = document.createElement('tr');
            let name = document.createElement('td');
            name.innerText = data[i].name;
            row.appendChild(name);
            let under = document.createElement('td');
            if (data[i].under){
                under.innerText = "Under";
            }
            else{
                under.innerText = "Nope";
            }
            row.appendChild(under);
            let chef = document.createElement('td');
            chef.innerText = data[i].chef.first_name + " " + data[i].chef.last_name;
            row.appendChild(chef);
            let actions = document.createElement('td');
            actions.innerHTML = `<a href="recipes/${data[i].id}">View Recipe</a>`
            if (data[i].users_id == session_user_id){
                actions.innerHTML += ` | <a href="/recipes/${data[i].id}">Edit</a> `
                actions.innerHTML += `| <a href="" onclick="destroy_recipe(${data[i].id});return false;">Delete</a>`
            }
            row.appendChild(actions);
            recipes.appendChild(row);
        }
}

async function get_new_recipe() {
    let response = await fetch('http://localhost:5000/read/new_recipe')
    let data = await response.json()
    let recipes = document.getElementById('recipes-table-body');
    let session_user_id = document.getElementById('users_id').value
    let row = document.createElement('tr');
    let name = document.createElement('td');
    name.innerText = data.name;
    row.appendChild(name);
    let under = document.createElement('td');
    if (data.under){
        under.innerText = "Under";
    }
    else{
        under.innerText = "Nope";
    }
    row.appendChild(under);
    let chef = document.createElement('td');
    chef.innerText = data.chef.first_name + " " + data.chef.last_name;
    row.appendChild(chef);
    let actions = document.createElement('td');
    actions.innerHTML = `<a href="recipes/${data.id}">View Recipe</a>`
    if (data.users_id == session_user_id){
        actions.innerHTML += ` | <a href="/recipes/edit/${data.id}">Edit</a> `
        actions.innerHTML += `| <a href="" onclick="destroy_recipe(${data.id});return false;">Delete</a>`
    }
    row.appendChild(actions);
    recipes.appendChild(row);
}

async function update_recipe() {
    let response = await fetch('http://localhost:5000/read/new_recipe')
    let data = await response.json()
    let recipe_info = document.getElementById('recipe-info');
    under_string = ""
    if (data.under){
        under_string = "Under"
    }
    else {
        under_string = "Nope"
    }
    recipe_info.innerHTML =
    `<tr>
        <td>Description:</td>
        <td>${data.description}</td>
    </tr>
    <tr>
        <td>Under 30 minutes?</td>
        <td>${under_string}</td>
    </tr>
    <tr>
        <td>Instructions:</td>
        <td>${data.instructions}</td>
    </tr>
    <tr>
        <td>Date Made:</td>
        <td>${data.date_made}</td>
    </tr>`
    let recipe_name = document.getElementById('recipe-name')
    let name = document.getElementById('name')
    recipe_name.innerText = data.name
    name.value = data.name
    let description = document.getElementById('description')
    description.value = data.description
    let instructions = document.getElementById('instructions')
    instructions.value = data.instructions
    let date_made = document.getElementById('date_made')
    date = new Date(data.date_made)
    date_made.value = date.toISOString().substring(0, 10)
    let under_yes = document.getElementById('under-yes')
    let under_no = document.getElementById('under-no')
    if (data.under) {
        under_yes.setAttribute("checked","")
        under_no.removeAttribute("checked")
    }
    else{
        under_no.setAttribute("checked","")
        under_yes.removeAttribute("checked")
    }
}

async function destroy_recipe(recipe_id) {
    let response = await fetch(`http://localhost:5000/recipes/destroy/${recipe_id}`)
    let data = await response.json()
    if (data["message"]) {
        let recipes = document.getElementById('recipes-table-body');
        recipes.innerHTML = ""
        get_recipes()
    }
    else{
        location.href = "/recipes"
    }
}