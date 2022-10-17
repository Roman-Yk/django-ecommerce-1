// const submitBtn = document.getElementById('login')
// var passwordField = document.getElementById('passwordfield')
// var emailField = document.getElementById('emailfield')

// submitBtn.addEventListener('click', function(){
//     var password = passwordField.value
//     var email = emailField.value

//     var url = 'http://127.0.0.1:8000/users/login_process/'
//     fetch(url, {
//         method:'POST',
//         headers:{
//             'Content-Type':'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({'password': password, 'email':email}),
//     })
    
//     .then((response)=>{
//         return response.json()
//     })

//     .then((data)=>{
//         console.log('data:', data)
//         if (data == "True"){
//             window.location.href = "http://127.0.0.1:8000/"
//         } else alert("That user doesn't exist")
//     })


// })


