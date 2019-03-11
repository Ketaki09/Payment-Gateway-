from flask import Flask, Response, request, session, render_template
import logging
import logging.config
from common.database_error import DatabaseError
from model.db_manager import DBManager
import uuid
import hashlib
import json
import secrets
import Validator
import time
import requests
from flask_wtf.csrf import CSRFProtect
from cryptography.fernet import Fernet
key = b"75aNEQkkFMwcw6qTagPo8LqjuiOwMrfSEr_acn_e_aA="
cipher_suite = Fernet(key)
csrf = CSRFProtect()
app = Flask(__name__)
logging.config.fileConfig("config/logging.conf")
app.secret_key = "project"


@app.route("/register", methods=['POST'])
def register_new_user():
    response = None
    try:
        content = request.json
        first_name = content['first_name']
        last_name = content['last_name']
        email = content['email']
        password = content['password']
        phone_number = content['phone_number']
        security_ans = content['security_ans']
        security_question_id = content['security_question_id']
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        card_number = cipher_suite.encrypt(content['card_number'].encode())
        card_expiry_month = content['card_expiry_month']
        card_expiry_year = content['card_expiry_year']
        card_name = content['card_name']
        # salt = uuid.uuid4().hex
        # hashed_password = hashlib.sha512(password + salt).hexdigest()

        db_manager = DBManager()

        if Validator.isValidName(first_name) and Validator.isValidName(last_name):
            if Validator.isValidEmail(email):
                if Validator.isValidPhoneNumber(phone_number):
                    if db_manager.get_profile_details_email(email) is None:
                        db_manager.register_user(first_name, last_name, email, phone_number,
                                                 password_hash, security_ans, security_question_id)
                        # TODO Call Bank API and verify card details before inserting into our db.
                        data = db_manager.get_id_from_email(email)
                        user_id = data[0]
                        db_manager.insert_payment(user_id, card_number, card_expiry_month, card_expiry_year, card_name)
                        response = {"status": "success"}
                    else:
                        response = {"status": "failed", "message": "User already exist"}
                else:
                    response = {"status": "failed", "message": "Phone no not valid"}
            else:
                response = {"status": "failed", "message": "Email not valid"}
        else:
            response = {"status": "failed", "message": "First name or Last name not valid"}

    except DatabaseError as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    except Exception as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    finally:
        if response is None:
            response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/login", methods=['POST'])
def login():
    response = None
    try:
        content = request.json
        email = content['email']
        password = content['password']
        authCode = content['authCode']
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if Validator.isValidEmail(email):
            db_manager = DBManager()
            result = db_manager.login_user(email, password_hash, authCode)
            if result is -1:
                response = {"status": "failed", "message": "Auth code expires generate new auth code"}
            elif result is None:
                response = {"status": "failed", "message": "Invalid Username or Password"}
            else:  
                data = json.loads(result)
                session['uid'] = uuid.uuid4()  # TODO Use strong pseudo random generator
                session['logged_in'] = True
                session['user_id'] = data['id']
                response = {"status": "success", "data": result}
    except ValueError as e:
        logging.exception(e)
        logging.info("Invalid Logon attempt for" + email)
        db_manager = DBManager()
        db_manager.invalid_login(email)
        response = {"status": "failed", "message": "Invalid Username or password"}
    except DatabaseError as e:
        logging.info("Invalid Logon attempt for" + email)
        logging.exception(e)
        db_manager = DBManager()
        db_manager.invalid_login(email)
        response = {"status": "failed", "message": "Invalid Username or password"}
    except Exception as e:
        logging.info("Invalid Logon attempt for" + email)
        logging.exception(e)
        db_manager = DBManager()
        db_manager.invalid_login(email)
        response = {"status": "failed", "message": "Invalid Username or password"}
    finally:
        if response is None:
            response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/securityquestion", methods=['GET'])
def security_question():
    response = None
    try:
        db_manager = DBManager()
        result = db_manager.get_security_questions()
        response = {"status": "success", "data": result}
    except DatabaseError as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    except Exception as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    finally:
        if response is None:
            response = {"status": "failed",
                        "message": "Unable to process the request. Please try again later"}
    return Response(json.dumps(response), mimetype='application/json')


@app.route('/logout', methods=['POST'])
def logout():
    response = None
    try:
        # TODO Input validations read id only from session.
        if session.get('uid') is not None:
            session.pop('uid', None)
            session.pop('logged_in', None)
            session.pop('user_id', None)
            response = {"status": "success"}
    except Exception as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    finally:
        if response is None:
            response = {"status": "failed",
                        "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/profile", methods=["GET", "POST"])
def profile_details():
    response = None
    try:
        content = request.json
        db_manager = DBManager()
        db_manager.update_profile_details(
            content["id"],
            content["first_name"]
        )
        response = {"status": "success"}
    except DatabaseError as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    except Exception as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    finally:
        if response is None:
            response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/transaction", methods=["POST"])
def transaction_details():
    response = None
    try:
        content = request.json
        if Validator.isValidDollarAmount(content["amount"]):
            db_manager = DBManager()
            payee_id = session["user_id"]
            data = db_manager.get_id_from_email(content['payer_id'])
            if data is None:
                response = {"status": "failed", "message": "Friend not registered"}
            else:
                payer_id = data[0]
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                db_manager.insert_transaction_details(payer_id, payee_id, content['amount'], 'Pending',now)
                response = {"status": "success"}
        else:
            response = {"status": "failed", "message": "Not a valid Amount"}
    except DatabaseError as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    except Exception as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    finally:
        if response is None:
            response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/approval", methods=["POST"])
def approval():
    response = None
    try:
        content = request.json
        db_manager = DBManager()
        user_id = db_manager.get_id_from_email(session["id"])
        payer_id = db_manager.get_id_from_email(content['payer_id'])
        db_manager.insert_transaction_details(payer_id, user_id, content['amount'], 'Pending')
        response = {"status": "success"}
    except DatabaseError as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    except Exception as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    finally:
        if response is None:
            response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return response


@app.route("/forget", methods=['POST'])
def client_email():
    content = request.json
    db_manager = DBManager()
    content = request.json
    result = db_manager.check_existing_email(content['email'])
    if result:
        gen_token = secrets.token_urlsafe()

        db_manager.update_db(content['verifyEmail'], gen_token)
        db_manager.send_email(content['verifyEmail'], gen_token)
        response = {"status": "success"}
    else:
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/invite_friend", methods=['POST'])
def invite_friend1():
    response = None
    db_manager = DBManager()
    content = request.json
    email = content['email']
    if email is not None:
        if Validator.isValidEmail(email):
            db_manager.send_email_invite_friend(email)
            response = {"status": "success"}
        else:
            response = {"status": "failed", "message": "Invalid email!"}
    else:
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/changepassword", methods=['GET'])
def check_token_expiry():
    #content = request.json
    db_manager = DBManager()
    token = request.args.get('token')
    result = db_manager.check_token_expiry(token)
    if result == -1:
        response = {"status": "failed", "message": "Token does not exist"}
    elif result == -2:
        response = {"status": "failed", "message": "Token does not match"}
    elif result == 1:
        response = {"status": "failed", "message": "Your Token is expired"}
    elif result == 2:
        response = {"status": "success", "message": "Token is valid"}
        return render_template("changepasswordlogout.html")
    return json.dumps(response)


@app.route("/makepayment", methods=["POST"])
def make_payment():
    try:
        content = request.json
        transaction_id = content['id']
        action = content['action']
        db_manager = DBManager()
        data = db_manager.get_single_transaction(transaction_id)
        amount = data['amount']
        payee_id = data['payee_id']
        payer_id = data['payer_id']
        if action == "Reject":
            db_manager.update_transaction_details(transaction_id, content['action'])
            response = {"status": "success"}
        else:
            # TODO Add error handling for each call
            data = db_manager.get_payment_details(payer_id)
            bank_data = {
                "card_number": cipher_suite.decrypt(data["card_number"].encode()).decode(),
                "expiry_month": data['card_expiry_month'],
                "expiry_year": data['card_expiry_year'],
                "name": data['card_name'],
                "amount": amount
            }
            deduct_bank_payment(bank_data)
            data = db_manager.get_payment_details(payee_id)
            bank_data = {
                "card_number": cipher_suite.decrypt(data["card_number"].encode()).decode(),
                "expiry_month": data['card_expiry_month'],
                "expiry_year": data['card_expiry_year'],
                "name": data['card_name'],
                "amount": amount
            }
            add_bank_payment(bank_data)

            db_manager.update_transaction_details(transaction_id, content['action'])
            response = {"status": "success"}
    except DatabaseError as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    except Exception as e:
        logging.exception(e)
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    finally:
        if response is None:
            response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)


@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


@app.route("/loginpage", methods=["GET"])
def login_page():
    return render_template('login.html')


@app.route("/invitefriend", methods=["GET"])
def invite_friend():
    return render_template('invitesuccess.html')


@app.route("/profilepage", methods=["GET"])
def profile_page():
    return render_template('profile.html')


@app.route("/tracker", methods=["GET"])
def tracker():
    db_manager = DBManager()
    incoming = db_manager.get_incoming_transactions(session['user_id'])
    outgoing = db_manager.get_outgoing_transactions(session['user_id'])
    return render_template('tracker.html', outgoing=outgoing, incoming=incoming)


@app.route("/payment", methods=["GET"])
def payment():
    return render_template('payment.html')


@app.route("/bill", methods=["GET"])
def bill():
    return render_template('bill.html')


@app.route("/pending", methods=["GET"])
def pending():
    return render_template('pending.html')


@app.route("/forgotpassword", methods=["GET"])
def forgot_password():
    return render_template('forgotpassword.html')


@app.route("/change_password", methods=["POST"])
def change_password1():
    db_manager = DBManager()
    content = request.json
    password_1 = content['password1']
    password_1 = hashlib.sha256(password_1.encode('utf-8')).hexdigest()
    db_manager.change_password(password_1)
    response = {"status": "success"}
    return json.dumps(response)

# @app.route("/changepassword", methods=["GET"])
# def change_password():
#     return render_template('changepassword.html')


def deduct_bank_payment(content):
    try:
        card_number = content['card_number']
        expiry_month = content['expiry_month']
        expiry_year = content['expiry_year']
        name = content['name']
        amount = content['amount']

        db_manager = DBManager()
        card_details = db_manager.get_bank_details(card_number)

        if card_details is None:
            raise ValueError("Invalid card details")

        if int(expiry_month) != int(card_details[4]) or int(expiry_year) \
                != int(card_details[5]):
            raise ValueError("Invalid card details")

        balance_amount = int(card_details[6] - int(amount))
        if balance_amount < 0:
            raise ValueError("Insufficient card balance")

        db_manager.update_bank_balance(card_details[0], balance_amount)

        response = {"status": "success"}
    except DatabaseError as e:
        logging.exception(e)
        raise ValueError("Unable to process the request")
    except Exception as e:
        logging.exception(e)
        raise ValueError("Unable to process the request")
    return True


def add_bank_payment(content):
    try:
        card_number = content['card_number']
        expiry_month = content['expiry_month']
        expiry_year = content['expiry_year']
        name = content['name']
        amount = content['amount']

        db_manager = DBManager()
        card_details = db_manager.get_bank_details(card_number)

        if card_details is None:
            raise ValueError("Invalid card details")

        if int(expiry_month) != int(card_details[4]) or int(expiry_year) \
                != int(card_details[5]):
            raise ValueError("Invalid card details")

        balance_amount = int(card_details[6] + int(amount))
        if balance_amount < 0:
            raise ValueError("Insufficient card balance")

        db_manager.update_bank_balance(card_details[0], balance_amount)

        response = {"status": "success"}
    except DatabaseError as e:
        logging.exception(e)
        raise ValueError("Unable to process the request")
    except Exception as e:
        logging.exception(e)
        raise ValueError("Unable to process the request")
    return True


@app.route("/sendcode", methods=['POST'])
def send_auth_code():
    response = None
    db_manager = DBManager()
    content = request.json
    email = content['email']
    if email is not None:
        if Validator.isValidEmail(email):
            if db_manager.get_profile_details_email(email) is not None:
                db_manager.send_email_auth_code(email)
                response = {"status": "success"}
            else:
                response = {"status": "failed", "message": "User Not found"}    
        else:
            response = {"status": "failed", "message": "Invalid email!"}
    else:
        response = {"status": "failed", "message": "Unable to process the request. Please try again later"}
    return json.dumps(response)




if __name__ == "__main__":
    csrf.init_app(app)
    app.run(ssl_context='adhoc')
