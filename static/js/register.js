// const submitBtn = document.getElementById('register')
// var passwordField = document.getElementById('passwordfield')
// var nameField = document.getElementById('namefield')
// var emailField = document.getElementById('emailfield')
// var passwordConfirm = document.getElementById('passwordfieldconf')
// var warning = document.getElementById('warning')
// var userExist = document.getElementById('userExist')

// submitBtn.addEventListener('click', function(){
//     var password = passwordField.value
//     var email = emailField.value
//     var name = nameField.value
//     var passwordConf = passwordConfirm.value

//     if (passwordConf == password){
//         var url = 'http://127.0.0.1:8000/users/register_process/'
//         fetch(url, {
//             method:'POST',
//             headers:{
//                 'Content-Type':'application/json',
//                 'X-CSRFToken': csrftoken,
//             },
//             body: JSON.stringify({'password': password, 'email':email, 'name': name}),
//         })
        
//         .then((response)=>{
//             return response.json()
//         })
    
//         .then((data)=>{
//             console.log('data:', data)
//             if(data == "Registrated"){
//                 window.location.href = "http://127.0.0.1:8000/"
//             }
//             if(data == "Exist"){
//                 userExist.classList.remove('hidden')
//             }
//         })
//     }  
//     else{
//         warning.classList.remove('hidden')
//     }


// })


