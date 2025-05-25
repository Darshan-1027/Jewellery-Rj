let Cancle = document.getElementById("close");
let Logout = document.getElementById("Logout");
let Card = document.getElementById("Card");

function Close(){

    Logout.style.display="none";
    Card.style.opacity="1";
    
}

function SureLogout(){

    Logout.style.display="block";

    Card.style.opacity="0.1";
      

}