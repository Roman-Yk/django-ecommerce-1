var updateBtns = document.getElementsByClassName('update-cart')

var cartTotal = document.getElementById('cart-total')
var cartTotalJs = cartTotal.textContent


for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)


        console.log('USER', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        }else
        {
            updateUserOrder(productId, action)
        }
    
    })
    
}


function addCookieItem(productId, action) {
    var totalItems = 0
    //get single item total value 
    var itemTotalPrice = document.querySelector(`[data-price="${productId}"]`)
    //get clear item price from itemTotalPrice
    var singleItemTotalPriceFloat = itemTotalPrice.textContent.replace('$','') 
    //get single item price
    var singlePrice = document.querySelector(`[data-singlePrice="${productId}"]`).textContent.replace('$', '')
    //get total Price of all items
    var totalPrice = document.getElementById("total-price")
    var totalPriceInt = parseFloat(totalPrice.textContent.replace('$', ''))
    if(action=='add'){
        console.log(singleItemTotalPriceFloat)
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
            //looping trough the cart to get total items
            for (const index in cart) {
                totalItems += cart[index]['quantity']
            }
            //set cart total items
            document.getElementById("itemsCount").innerHTML = totalItems
            //set cart total items for navbar
            document.getElementById("cart-total").innerHTML = totalItems
            //set single item price
            itemTotalPrice.innerHTML = '$'+(parseFloat(singleItemTotalPriceFloat) + parseFloat(singlePrice)).toFixed(2)
        }else{
            cart[productId]['quantity'] += 1
            //looping trough the cart to get total items
            for (const index in cart) {
                totalItems += cart[index]['quantity']
            }
            //set cart total items
            document.getElementById("itemsCount").innerHTML = totalItems
            //set cart total items for navbar
            document.getElementById("cart-total").innerHTML = totalItems
            //Set exact product quantity
            document.querySelector(`[data-quantity="${productId}"]`).innerHTML =  cart[productId]['quantity']
            //set single item total price
            itemTotalPrice.innerHTML = '$'+(parseFloat(singleItemTotalPriceFloat) + parseFloat(singlePrice)).toFixed(2)
            //adding single item price to total price
            totalPriceInt += parseFloat(singlePrice)
            //set total price
            totalPrice.innerHTML = '$' + totalPriceInt.toFixed(2)
        }
    }

    if(action == "remove"){
        cart[productId]['quantity'] -= 1
        //looping trough the cart to get total items
        for (const index in cart) {
            totalItems += cart[index]['quantity']
        }
        //set cart total items
        document.getElementById("itemsCount").innerHTML = totalItems
        //set cart total items for navbar
        document.getElementById("cart-total").innerHTML = totalItems
        //Set exact product quantity
        document.querySelector(`[data-quantity="${productId}"]`).innerHTML =  cart[productId]['quantity']
        //set single item total price
        itemTotalPrice.innerHTML = '$'+(parseFloat(singleItemTotalPriceFloat) - parseFloat(singlePrice)).toFixed(2)
        //removing single item price to total price
        totalPriceInt -= parseFloat(singlePrice)
        //set total price
        totalPrice.innerHTML = '$' + totalPriceInt.toFixed(2)

        // check if quantity is greater than 0 if not, then remove item
        if(cart[productId]['quantity'] <= 0){
            document.querySelector(`[data-itemId="${productId}"]`).remove()
            console.log("Remove Item")
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    //location.reload()
}


function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data ...')
    if(action == "add"){
        cartTotalJs = parseInt(cartTotalJs)
        cartTotalJs +=1
        
    }
    if(action == "remove"){
        cartTotalJs = parseInt(cartTotalJs)
        cartTotalJs -= 1
    }

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data:', data)
        cartTotal.innerHTML = cartTotalJs

        //Get exact product quantity
        var productQuantity = data['itemQuantity']

        //Check if items quanitity is greater than 0 if not, remove
        if(productQuantity <=0 ){
            //If product quantity <= 0 remove whole card
           document.querySelector(`[data-itemId="${productId}"]`).remove()

           //set cart total price because if we not set it the new walue will be display only after page reloading
            document.getElementById("total-price").innerHTML = '$'+data['total']
           
        }
        else{
            //If product quantity > 0 then set new value
            document.querySelector(`[data-quantity="${productId}"]`).innerHTML = productQuantity

            //set cart total price
            document.getElementById("total-price").innerHTML = '$'+data['total']
        }
        
        //set total quantity
        document.getElementById("itemsCount").innerHTML = data['items']
        //set product total price
        document.querySelector(`[data-price="${productId}"]`).innerHTML = '$'+data['productPrice']   
        
        //   //Check if total quantity is greater than 0 to display data correctly when it's 0
        //   if(data['items'] <= 0){
        //     //set total quantity
        //     document.getElementById("itemsCount").innerHTML = '0'
        //     //set product total price
        //     document.querySelector(`[data-price="${productId}"]`).innerHTML = '$0.00' 
        // }
        // else{
        //      //set total quantity
        //     document.getElementById("itemsCount").innerHTML = data['items']
        //     //set product total price
        //     document.querySelector(`[data-price="${productId}"]`).innerHTML = data['productPrice']   
        // }
    })
}






