function registerUser(data){
    let request = new XMLHttpRequest();
    request.open("POST", "/register", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}
function loginService(data){
    let request = new XMLHttpRequest();
    request.open("POST", "/login", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}

function logoutService(data){
    let request = new XMLHttpRequest();
    request.open("POST", "/logout", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}
function verifyEmail(data){
    let request = new XMLHttpRequest();
    request.open("POST", "/forget", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        alert(response["Password recovery email has been sent to your registered email id"]);
        return true
    }else{
        alert(response["message"]);
        return false
    }
}

function requestEmail(data){
    let request = new XMLHttpRequest();
    request.open("POST", "/invite_friend", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}

function addTransaction(data){
    let request = new XMLHttpRequest();
    request.open("POST", "/transaction", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}


function verifyPayment(data){
    request = new XMLHttpRequest();
    request.open("POST", "/payment", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}

function transactionService(data){
    let request = new XMLHttpRequest();
    request.open("POST", "/makepayment", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}

function verifyPassword(data){
    request = new XMLHttpRequest();
    request.open("POST", "/change_password_logout", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}
function verifyLogoutPassword(data){
    request = new XMLHttpRequest();
    let request = new XMLHttpRequest();
    request.open("POST", "/change_password", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    response = JSON.parse(request.response)

    let response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    }else{
        alert(response["message"]);
        return false
    }
}

function sendAuthCodeEmail(data) {
    request = new XMLHttpRequest();
    request.open("POST", "/sendcode", false);
    let csrf_token = document.getElementById("csrf_token").value
    request.setRequestHeader("X-CSRFToken", csrf_token);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.send(JSON.stringify(data));
    response = JSON.parse(request.response)
    if (response["status"]=="success"){
        return true
    } else if (response["status"]=="failed") {
        return false
    } else {
        alert(response["message"]);
        return false
    }
}
