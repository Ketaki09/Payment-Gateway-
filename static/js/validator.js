/*
All take a String as input, can edit or add wrapper functions to use input from forms 
All return true is valid, false otherwise
*/

//has to be gmail
function isValidEmail (email) {
    var emailEnd = email.substring(email.length - 10);
    var emailStart = email.substring(0, email.length - 10);
    var i;
    
    //ends with @gmail.com
    if (emailEnd != "@gmail.com") {
        return false;
    }

    //uses only letters numbers and periods
    var re = /[a-zA-Z0-9\.]/;
    for (i = 0; i < emailStart.length; i++) {
        if (!re.test(emailStart.substring(i, i+1))) {
            return false;
        }
    }

    //6-30 characters (not counting . or @gmail.com)
    var count = 0;
    for (i = 0; i < emailStart.length; i++) {
        if (emailStart.charAt(i) != '.') {
            count++;
        }
    }
    if (count < 6 || count > 30) {
        return false;
    }

    //first and last char must be letter or number
    re = /^[a-zA-Z0-9]/;
    if (!re.test(emailStart)) {
	    return false;
    }
    re = /[a-zA-Z0-9]$/;
    if (!re.test(emailStart)) {
	    return false;
    }

    //no consecutive periods
    re = /\.\./;
    if (re.test(emailStart)) {
	    return false;
    }

    //8 or more chars must contain a letter
    if (count > 8) {
        re = /[a-zA-Z]/;
        if (!re.test(emailStart)) {
            return false;
        }
    }

    return true;
}

/*
Assumptions for a valid name (subject to change):
    Only letters, no more than three spaces, 0-2 non-consecutive or each hyphen, period, and single-quote
    length has 1-50 letters
*/
function isValidName (name) {
    var letCount = 0;
    var spaceCount = 0;
    var re = /[a-zA-Z\-\. ']/;
    var relets = /[a-zA-Z]/;
    for (var i = 0; i < name.length; i++) {
        if (!re.test(name.substring(i, i+1))) {
            return false;
        }
        if (relets.test(name.substring(i, i+1))) {
            letCount++;
        } else if (name.charAt(i) == ' ') {
            spaceCount++;
        }
    }
    if (letCount < 1 || letCount > 50 || spaceCount >3) {
        return false;
    }
    re = /\-.*\-.*\-.*/;
    if (re.test(name)) {
        return false;
    }
    re = /\..*\..*\./;
    if (re.test(name)) {
        return false;
    }
    re = /'.*'.*'/;
    if (re.test(name)) {
        return false;
    }
    re = /\.\./;
    if (re.test(name)) {
        return false;
    }
    re = /''/;
    if (re.test(name)) {
        return false;
    }
    re = /--/;
    if (re.test(name)) {
        return false;
    }
    return true;
}

/*
may have a leading +
may have one set of (), with 2-3 numbers inside
may have to to 3 (non-consecutive) dashes, spaces or parenthesis
all other characters must be numbers
must end in a group of at least four numbers
[5, 18] total characters
*/
function isValidPhoneNumber (phone) {
    //remove leading + if it exists
    if (phone.charAt(0) == '+') {
	    phone = phone.substring(1);
    }

    //correct length
    if (phone.length < 5 || phone.length > 18) {
        return false;
    }

    //valid chars
    var maxSpaceDashParen = 3;
    var openParenIndex = -1;
    var closeParenIndex = -1;
    var re = /[0-9\-\(\) ]/;
    for (var i = 0; i < phone.length; i++) {
        if (!re.test(phone.substring(i, i+1))) {
            return false;
        }
        if (phone.charAt(i) == '(') {
            if (openParenIndex != -1 || i > 3 || maxSpaceDashParen != 3) {
                return false;
            }
            openParenIndex = i;
            maxSpaceDashParen = 1;
        }
        else if (phone.charAt(i) == ')') {
            if (closeParenIndex != -1 || openParenIndex == -1) {
                return false;
            }
            if (maxSpaceDashParen != 1) {
                return false;
            }
            closeParenIndex = i;
        }
        else if (phone.charAt(i) == '-') {
            maxSpaceDashParen--;
        }
        else if (phone.charAt(i) == ' ') {
            maxSpaceDashParen--;
        }
    }

    if (maxSpaceDashParen < 0) {
        return false;
    }
    re = /--/;
    if (re.test(phone)) {
        return false;
    }
    re = /  /;
    if (re.test(phone)) {
        return false;
    }

    // 2-3 numbers inside parenthesis 
    var numInParen = closeParenIndex - openParenIndex;
    if ((numInParen != 4) && (numInParen != 3) && (numInParen != 0)) {
        return false;
    }

    //ends in 4 numbers
    re = /[0-9]{4}$/;
    if (!re.test(phone)) {
        return false;
    }

    return true;
}

/*
valid card number formats:
    #### #### #### ####
    ####-####-####-####
    ################
*/
function isValidCardNumber (number) {
    var re = /[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}/;
    if ((number.length == 19) && (re.test(number))) {
        return true;
    }

    re = /[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}/;
    if ((number.length == 19) && (re.test(number))) {
        return true;
    }

    re = /[0-9]{16}/;
    if ((number.length == 16) && (re.test(number))) {
        return true;
    }

    return false;
}

//4 digits America Express, 3 otherwise
function isValidCVV (cvv) {
    var re = /[0-9]{4}/;
    if ((cvv.length == 4) && (re.test(cvv))) {
        return true;
    }
    re = /[0-9]{3}/;
    if ((cvv.length == 3) && (re.test(cvv))) {
        return true;
    }
    return false;
}

/*
letters and numbers for now, can change latter
length between 1 - 50, can also change later
*/
function isValidUserID (id) {
    var re = /[a-zA-Z0-9]/;
    for (var i = 0; i < id.length; i++) {
        if (!re.test(id.substring(i, i+1))) {
            return false;
        }
    }
    if (id.length < 1 || id.length > 50) {
        return false;
    }
    return true;
}

/*
security question answer
letters, numbers, spaces (not consecutive)
length between 1-50
*/
function isValidAnswer (ans) {
    var re = /[a-zA-Z0-9 ]/;
    for (var i = 0; i < ans.length; i++) {
        if (!re.test(ans.substring(i, i+1))) {
            return false;
        }
    }
    if (ans.length < 1 || ans.length > 50) {
        return false;
    }
    re = /  /;
    if (re.test(ans)) {
        return false;
    }
    return true;
}

//calender dates (MM/DD/YYYY)
function isValidDate(date) {
    var re = /[0-1][0-9]\/[0-3][0-9]\/[1-2][0-9]{3}/;
    if ((date.length == 10) && (re.test(date))) {
        return true;
    }
    return false;
}

/*
only numbers, possible leading $, and possible tailing .##
setting a cap at $9999.99
*/
function isValidDollarAmount (money) {
    //check for $
    if (money.charAt(0) == '$') {
        money = money.substring(1);
    }
    //check for cents
    var re = /\.[0-9]{2}/;
    if (re.test(money.substring(money.length-3))) {
        money = money.substring(0, money.length-3);
    }
    if (money.length > 4) {
        return false;
    }
    re = /[0-9]/;
    for (var i = 0; i < money.length; i++) {
        if (!re.test(money.substring(i, i+1))) {
            return false;
        }
    }
    return true;
}

/*
Google authenticator code
six digit number (I think)
### ### or ######
*/
function isValidCode (code) {
    var re = /[0-9]{3} [0-9]{3}/;
    if ((code.length == 7) && (re.test(code))) {
        return true;
    }
    re = /[0-9]{6}/;
    if ((code.length == 6) && (re.test(code))) {
        return true;
    }
    return false;
}

/*
password
checks length, 8-50 characters
*/
function isValidPassWord (passWord) {
    if (passWord.length < 8 || passWord.length > 50) {
        return false;
    }
    return true;
}
/*
token to change email is logged out
23 alphanumeric characters
*/
function isValidToken(token) {
    re = /[0-9]{23}/;
    if ((token.length == 23) && (re.test(token))) {
        return true;
    }
    return false;
}

//TODO: security question (possibly)

/*
just alert for now, can make it prettier after validation works with html
*/
function badThingHappened (message) {
    alert(message);
}

/*
validate sign up (page 1)
reference https://www.w3schools.com/js/js_validation.asp
*/
function validateSignUp () {
    //first name 
    var fname = document.forms["sign-in"]["firstname"].value;
    if (!isValidName (fname)) {
        badThingHappened("Invalid input for first name");
        return false;
    }

    //last name
    var lname = document.forms["sign-in"]["lastname"].value;
    if (!isValidName (lname)) {
        badThingHappened("invalid input for last name");
        return false;
    }

    //email
    var email = document.forms["sign-in"]["email"].value;
    if (!isValidEmail (email)) {
        badThingHappened("Invalid input for gmail");
        return false;
    }

    //card no
    var card_number = document.forms["sign-in"]["card_number"].value;
    if (!isValidCardNumber (card_number)) {
        badThingHappened("Invalid input for credit card");
        return false;
    }

    //phone
    var phone = document.forms["sign-in"]["phone"].value;
    if (!isValidPhoneNumber (phone)) {
        badThingHappened("Invalid input for phone number");
        return false;
    }

    //password
    var password = document.forms["sign-in"]["password"].value;
    if (!isValidPassWord (password)) {
        badThingHappened("Invalid input for passowrd");
        return false;
    }

    //TODO: question  no front end question check yet, will whitelist options

    //answer    (use name validator)
    var answer = document.forms["sign-in"]["answer"].value;
    if (!isValidName (fname)) {
        badThingHappened("Invalid input for answer");
        return false;
    }
    let data = {
        "first_name" : fname,
        "last_name" : lname,
        "email" : email,
        "phone_number" : phone,
        "password" : password,
        "security_ans" : answer,
        "security_question_id": 1, //TODO Map security question id
        "card_number": document.forms["sign-in"]["card_number"].value,
        "card_expiry_month": document.forms["sign-in"]["card_expiry_month"].value,
        "card_expiry_year": document.forms["sign-in"]["card_expiry_year"].value,
        "card_name": document.forms["sign-in"]["card_name"].value
    }
    if (registerUser(data) == true){
        window.location = "/loginpage";
    }
    return true;
}

function validateLogout(){
    //No Validation necessary. Directly call service
    logoutService({})
    window.location = "/loginpage"
}

/*
validate make payment (page 4)
*/
function validateMakePayment () {
    //userid
    var email = document.forms["pay"]["email"].value;
    if (!isValidEmail (email)) {
        badThingHappened("Invalid input for email");
        return false;
    }

    //name 
    var fname = document.forms["pay"]["name"].value;
    if (!isValidName (fname)) {
        badThingHappened("Invalid input for name");
        return false;
    }

    //phone
    var phone = document.forms["pay"]["phone"].value;
    if (!isValidPhoneNumber (phone)) {
        badThingHappened("Invalid input for phone number");
        return false;
    }

    //TODO:  no front end validation for card yet

    //TODO: success page?
    data = {
        "email": email,
        "first_name": fname,
        "phone": phone
    }
    window.location = "payment";
    return true;
}

// page 5 (part 1)
function validateShareBill () {
    //amount
    var money = document.forms["shair"]["money"].value;
    if (!isValidDollarAmount (money)) {
        badThingHappened("Invalid input for amount");
        return false;
    }

    //username or email
    var payer_id = document.forms["shair"]["payer_id"].value;
    if ((!isValidName (payer_id)) && (!isValidEmail(payer_id))) {
        badThingHappened("Invalid input for username or email");
        return false;
    }

    data = {
        "amount": money,
        "payer_id": payer_id
    }
    if(addTransaction(data)==true){
        window.location = "tracker";
    }
    return true;
}

// page 5 (part 2)
function validateRequest () {
    //amount
    var money = document.forms["request"]["money"].value;
    if (!isValidDollarAmount (money)) {
        badThingHappened("Invalid input for amount");
        return false;
    }

    //username or email
    var identifier = document.forms["request"]["identifier"].value;
    if ((!isValidName (identifier)) && (!isValidEmail(identifier))) {
        badThingHappened("Invalid input for username or email");
        return false;
    }

    //to pay (what they are paying for i think)
    var fname = document.forms["request"]["topay"].value;
    if (!isValidName (fname)) {
        badThingHappened("Invalid input for To Pay");
        return false;
    }

    //phone
    var phone = document.forms["request"]["phone"].value;
    if (!isValidPhoneNumber (phone)) {
        badThingHappened("Invalid input for phone number");
        return false;

    }

    //TODO: success page
    window.location = "bill";
    return true;
}

function validateLogIn() {
    //email
    var email = document.forms["login"]["email"].value;
    if (!isValidEmail (email)) {
        badThingHappened("Invalid input for gmail");
        return false;
    }

    //password
    var password = document.forms["login"]["password"].value;
    if (!isValidPassWord (password)) {
        badThingHappened("Invalid input for password");
        return false;
    }

    //google auth code
    var code = document.forms["login"]["code"].value;
    if (!isValidCode (code)) {
        badThingHappened("Invalid input for Google Authentication Code");
        return false;
    }
    let data = {
        "email": email,
        "password" : password,
        "authCode" : code 
    }
    if (loginService(data) == true){
      window.location = "/";
    }
    return true;
}

function validatePasswordChangeLoggedIn() {
    var password1 = document.forms["changepass1"]["new"].value;
    if (!isValidPassWord (password1)) {
        badThingHappened("Invalid input for first passowrd");
        return false;
    }

    var password2 = document.forms["changepass1"]["verify"].value;
    if (!isValidPassWord (password2)) {
        badThingHappened("Invalid input for second passowrd");
        return false;
    }

    if(password1 != password2 ) {
        badThingHappened("Passwords do not match");
        return false;
    }
    let data ={
        'password1': password1
    }
    if(verifyPassword(password1, password2) == true){
        window.location = "/loginpage";
    }



    return true;
}

function validatePasswordChangeNotLoggedIn() {
    //email
    var email = document.forms["changepass2"]["email"].value;
    if (!isValidEmail (email)) {
        badThingHappened("Invalid input for email");
        return false;
    }
    let data ={
        'email': email
    }
    window.location = "/loginpage";

    return true;
}

function validateSendEmail() {
    var email = document.forms["changepass2"]["email"].value;
    if (!isValidEmail (email)) {
        badThingHappened("Invalid input for email");
        return false;
    }
    data={
        "email": email
    }
    if (verifyEmail(data) == true){
        window.location = "/";
    }
    return true;
}

function updateTransaction(id, action){
    let data = {
        "id": id,
        "action": action
    }
    if(transactionService(data)==true){
        window.location = "tracker";
    }
}

function validateInviteFriend() {
    var email = document.forms["invite_email"]["email"].value;
    if (!isValidEmail (email)) {
        badThingHappened("Invalid input for email");
        return false;
    }
    data={
        "email": email
    }
    if(requestEmail(data) == true) {
        window.location = "/";
    }
    return true;
}

function validatePasswordChangeLoggedout(){
    var password1 = document.forms["changepass2"]["new"].value;
    if (!isValidPassWord (password1)) {
        badThingHappened("Invalid input for first passowrd");
        return false;
    }

    var password2 = document.forms["changepass2"]["verify"].value;
    if (!isValidPassWord (password2)) {
        badThingHappened("Invalid input for second passowrd");
        return false;
    }

    if(password1 != password2 ) {
        badThingHappened("Passwords do not match");
        return false;
    }
    let data={
        "password1": password1,
        "password2": password2
    }
    if(verifyLogoutPassword(data) == true){
        window.location = "/profilepage";
    }
    return true
}

function sendAuthCode(data) {
    var email = document.forms["login"]["email"].value;
    if (!isValidEmail (email)) {
        badThingHappened("Invalid input for email");
        return false;
    }
    data={
        "email": email
    }
    if(sendAuthCodeEmail(data) == true) {
        window.location = "/";
    } else {
        badThingHappened("Invalid input for email")
    }
    return true;
}