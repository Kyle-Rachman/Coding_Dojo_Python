if (window.location.href == 'http://localhost:5000/'){
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