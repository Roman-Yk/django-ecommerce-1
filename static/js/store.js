
function filterProduct(value){
    let buttons = document.querySelectorAll(".category-button")

    buttons.forEach((button) => {
        if(value.toUpperCase() == button.innerText.toUpperCase()){
            button.classList.add("active-category");
        }
        else{
            button.classList.remove("active-category");
        }
    });

    //select all cards
    let elements = document.querySelectorAll(".card-product");
    // loop through all cards
    elements.forEach((element) => {
        //display all cards on 'all' button click
        if(value == "all"){
            element.classList.remove("hidden");
        }
        else{
            //Check if element contains category class
            if(element.classList.contains(value)){
                //Display element based on category
                element.classList.remove("hidden");
            }
            else{
                element.classList.add("hidden");
            }
        }
    })
}

window.onload = () => {
    filterProduct('all')
}

var open = false

function burger(){
    open = !open
    var active_filter = document.getElementById('active_filter')
    var divs = document.getElementsByClassName('lines')
    if(open){
        active_filter.style.transform = 'scale(1,1)'
        active_filter.style.transitionDuration = '0.5s'
        counter = 0
        for (const child of divs) {
            child.style.backgroundColor = 'black'
            //Transform burger into cross
            if(counter == 0){
                child.style.transform = "rotate(45deg)"
                child.style.position = 'absolute'
                child.style.top = "9px"
            }
            if(counter == 1){
                child.style.display = "none"
            }
            if(counter == 2){
                child.style.transform = "rotate(-45deg)"
            }
            counter += 1
          }
    }
    else{
        active_filter.style.transform = 'scale(1,0)'
        active_filter.style.transitionDuration = '0.5s'
        counter = 0
        for (const child of divs) {
            child.style.backgroundColor = 'white'
            //Transform burger into cross
            if(counter == 0){
                child.style.transform = "rotate(0deg)"
                child.style.position = 'relative'
                child.style.top = "0px"
            }
            if(counter == 1){
                child.style.display = "block"
            }
            if(counter == 2){
                child.style.transform = "rotate(0deg)"
            }
            counter += 1
          }
    }

}



