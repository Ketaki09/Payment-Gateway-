import sys
import mysql.connector
import logging
import json
import smtplib
from common.database_error import DatabaseError
from config.database_config import connection_details
from config.email_config import connection_email_details
from datetime import datetime
from cryptography.fernet import Fernet
import itertools
import random
import time

sys.path.append('./config')


class DBManager:
    def __init__(self):
        self.conn = None

    def get_connection(self):
        cipher = Fernet('75aNEQkkFMwcw6qTagPo8LqjuiOwMrfSEr_acn_e_aA=')

        self.conn = mysql.connector.connect(
            host = cipher.decrypt(connection_details['host'].encode()).decode(),
            user = cipher.decrypt(connection_details['username'].encode()).decode(),
            password = cipher.decrypt(connection_details['password'].encode()).decode(),
            database = cipher.decrypt(connection_details['database'].encode()).decode()
        )

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()

    def check_token(self, token):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            logging.info(token)
            temp = token.split("/")
            id=temp[0]
            token = temp[1]
            sql_parameterized_query = "select ctoken, ccipher from clienttoken where id = %s"
            input_values = (id,)
            cursor.execute(sql_parameterized_query, input_values)
            x = cursor.fetchall()
            logging.info("check token")
            logging.info(x)
            ctoken = x[0][0]
            logging.info(x)
            key = x[0][1]           #cipher key
            key = Fernet(key)
            token = token.encode()
            decrypt = key.decrypt(token)
            logging.info(decrypt)
            logging.info(ctoken)
            if decrypt.decode() == ctoken:
                logging.info("Token matches")
                return (True,ctoken)
            else:
                logging.info("Token does not match")
                return False
        except IndexError as error:
            logging.info("The Token does not exist")
            raise IndexError(error)
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def getid(self, email):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            sql_parameterized_query = "select id from clienttoken where email = %s"
            input_values = (email,)
            cursor.execute(sql_parameterized_query, input_values)
            x = cursor.fetchall()
            return x[0][0]
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def send_email(self, email, gen_token):
        cipher_key = Fernet.generate_key()
        cipher = Fernet(cipher_key)
        text = gen_token.encode()
        encrypt = cipher.encrypt(text)
        logging.info("From send email")

        self.update_db(email, gen_token, cipher_key)
        try:
            id = self.getid(email)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(connection_email_details['email'], connection_email_details['password'])
            text_to_send = "http://127.0.0.1:5000/changepassword?token="+str(id)+"/"+encrypt.decode()
            msg = 'Subject: {}\n\n{}'.format("Temporary Password for Online Payment Portal", text_to_send)
            server.sendmail(connection_email_details['email'], email, msg)
        except smtplib.SMTPConnectError as error:
            raise smtplib(error)



    def send_email_invite_friend(self, email_1):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(connection_email_details['email'], connection_email_details['password'])

        msg = 'Subject: {}'.format("Hey, Your friend has invited you to use ONLINE PAYMENT PORTAL.")
        server.sendmail(connection_email_details['email'], email_1, msg)


    def check_token_expiry(self, token):
        try:
            logging.info(1)
            val_token, token = self.check_token(token)
            if val_token:
                self.get_connection()
                cursor = self.conn.cursor()
                sql_parameterized_query = "select ctime from clienttoken where ctoken = %s"
                input_values = []
                input_values.append(token)
                cursor.execute(sql_parameterized_query, input_values)
                x = cursor.fetchall()
                dt = datetime.strptime(str(x[0][0]), '%Y-%m-%d %H:%M:%S')
                m = dt.timestamp() * 1000
                n = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dt = datetime.strptime(n, '%Y-%m-%d %H:%M:%S')
                n = dt.timestamp() * 1000
                if(n - m) > 300000:
                    logging.info("Expired the key")
                    return 1
                else:
                    logging.info("token is valid")
                    return 2
            elif val_token == -1:
                return -1
            else:
                return -2
        except IndexError as error:
            logging.info("The Token does not exist")
            raise IndexError(error)
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def update_db(self, email, gen_token, cipher):
        try:
            result = self.check_existing_email(email)
            if result:
                self.get_connection()
                cursor = self.conn.cursor()
                sql_parameterized_query = "insert into clienttoken (email ,ctoken, ccipher) values(%s, %s, %s ) "
                input_values = (email ,gen_token, cipher)
                cursor.execute(sql_parameterized_query, input_values)
                self.conn.commit()
        except mysql.connector.Error as error:
            logging.error("Error occurred at get_profile_details", error)
            raise DatabaseError("Unable to retrieve user details")
        finally:
            self.close_connection()

    def check_existing_email(self, email):
        try:
            self.get_connection()
            cursor = self.conn.cursor()
            sql_parameterized_query = "select email from users where email = %s"
            input_values = (email,)
            cursor.execute(sql_parameterized_query, input_values)
            email_result = cursor.fetchall()
            try:
                if email_result[0][0] == email:
                    logging.info("User is registered")
                    uresult = True
            except IndexError as error:
                logging.info("User is not registered")
                return False
                raise IndexError(error)
            # TODO check if the user has already used forget password link
            if uresult:
                try:
                    sql_parameterized_query = "select email from clienttoken where email = %s"
                    input_values = (email,)
                    cursor.execute(sql_parameterized_query, input_values)
                    result = cursor.fetchall()
                    if result[0][0] == email:
                        sql_parameterized_query = "delete from clienttoken where email = %s"
                        cursor.execute(sql_parameterized_query, input_values)
                        self.conn.commit()
                        return True
                except IndexError:
                    return True

        except mysql.connector.Error as error:
            logging.error("Error occurred at get_profile_details", error)
            raise DatabaseError("Unable to retrieve user details")
        finally:
            self.close_connection()

    def get_profile_details(self, user_id):
        try:
            self.get_connection()
            logging.info("Entered get_profile_details")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select first_name, last_name, 
            email, phone_number, security_question_id, security_ans, 
            id from users where id = %s"""
            input_values = (user_id,)
            cursor.execute(sql_parameterized_query, input_values)
            row_headers = [header[0] for header in cursor.description]
            result = cursor.fetchone()
            if result is None:
                return result
            json_data = [(dict(zip(row_headers, result)))]
            logging.info("Exited get_profile_details")
            return json.dumps(json_data[0])
        except mysql.connector.Error as error:
            logging.error("Error occurred at get_profile_details", error)
            raise DatabaseError("Unable to retrieve user details")
        finally:
            self.close_connection()

    def get_profile_details_email(self, email):
        try:
            self.get_connection()
            logging.info("Entered get_profile_details_email")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select * from users where email = %s"""
            input_values = (email,)
            cursor.execute(sql_parameterized_query, input_values)
            row_headers = [header[0] for header in cursor.description]
            result = cursor.fetchone()
            if result is None:
                return result
            json_data = [(dict(zip(row_headers, result)))]
            logging.info("Exited get_profile_details_email")
            return json.dumps(json_data[0])
        except mysql.connector.Error as error:
            logging.error("Error occurred at get_profile_details_email", error)
            raise DatabaseError("Unable to retrieve user details")
        finally:
            self.close_connection()

    def get_security_questions(self):
        try:
            self.get_connection()
            logging.info("Entered get_profile_details")
            cursor = self.conn.cursor()
            sql_parameterized_query = "select id,question from security_question"
            cursor.execute(sql_parameterized_query)
            result = cursor.fetchall()
            logging.info("Exited get_profile_details")
            return result
        except mysql.connector.Error as error:
            logging.error("Error occurred at get_profile_details", error)
            raise DatabaseError("Unable to retrieve user details")
        finally:
            self.close_connection()

    def update_profile_details(
            self,
            user_id,
            first_name,
            last_name,
            email,
            phone_number,
            security_question_id,
            security_ans):
        try:
            self.get_connection()
            logging.info("Entered update_profile_details")
            cursor = self.conn.cursor()
            sql_parameterized_query = """update users set first_name = %s,
                                            last_name = %s, email = %s, phone_number = %s,
                                            security_question_id = %s, security_ans = %s  where id = %s"""
            input_values = (first_name, last_name, email, phone_number, security_question_id, security_ans, user_id)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
            logging.info("Exited update_profile_details")
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def get_incoming_transactions(self, id):
        try:
            self.get_connection()
            logging.info("Entered get_incoming_transactions")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select trn.payer_id, trn.payee_id, trn.id, trn.amount, trn.status
            from transaction trn,users usrs where usrs.id = trn.payee_id and usrs.id = %s"""
            input_values = (id,)
            cursor.execute(sql_parameterized_query, input_values)
            result = cursor.fetchall()
            data = []
            for row in result:
                record = {
                    "payer_id": row[0],
                    "payee_id": row[1],
                    "id": row[2],
                    "amount": row[3],
                    "status": row[4]
                }
                data.append(record)
        except mysql.connector.Error as error:
            logging.error("Error occurred at get_transaction_details", error)
            raise DatabaseError("Unable to retrieve transaction details")
        return data

    def get_outgoing_transactions(self, id):
        try:
            self.get_connection()
            logging.info("Entered get_transaction_details")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select trn.payer_id, trn.payee_id, trn.id, trn.amount, trn.status
            from transaction trn,users usrs where usrs.id = trn.payer_id and usrs.id = %s"""
            input_values = (id,)
            cursor.execute(sql_parameterized_query, input_values)
            result = cursor.fetchall()
            data = []
            for row in result:
                record = {
                    "payer_id": row[0],
                    "payee_id": row[1],
                    "id": row[2],
                    "amount": row[3],
                    "status": row[4]
                }
                data.append(record)
        except mysql.connector.Error as error:
            logging.error("Error occurred at get_transaction_details", error)
            raise DatabaseError("Unable to retrieve transaction details")
        return data

    def get_single_transaction(self, transaction_id):
        try:
            self.get_connection()
            logging.info("Entered get_incoming_transactions")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select trn.payer_id, trn.payee_id, trn.id, trn.amount, trn.status
            from transaction trn where trn.id = %s"""
            input_values = (transaction_id,)
            cursor.execute(sql_parameterized_query, input_values)
            row_headers = [header[0] for header in cursor.description]
            result = cursor.fetchone()
            json_data = [(dict(zip(row_headers, result)))]
            logging.info("Exited get_single_transactions")
            return json_data[0]

        except mysql.connector.Error as error:
            logging.error("Error occurred at get_transaction_details", error)
            raise DatabaseError("Unable to retrieve transaction details")
        return data

    def update_transaction_details(
                self,
                transaction_id,
                status
            ):
            try:
                self.get_connection()
                logging.info("Entered update_transaction_details")
                cursor = self.conn.cursor()
                sql_parameterized_query = """update transaction set status = %s where id = %s"""
                input_values = (status, int(transaction_id))
                cursor.execute(sql_parameterized_query, input_values)
                self.conn.commit()
                logging.info("Exited update_transaction_details")
            except mysql.connector.Error as error:
                self.conn.rollback()
                raise DatabaseError(error)
            finally:
                self.close_connection()

    def insert_transaction_details(
                self,
                payer_id,
                payee_id,
                amount,
                status,
                time
            ):
            try:
                self.get_connection()
                logging.info("Entered insert_transaction_details")
                cursor = self.conn.cursor()
                sql_parameterized_query = """insert into transaction(payer_id, payee_id, amount, status, timestamp)
                values(%s, %s, %s, %s, %s)"""
                input_values = (payer_id, payee_id, amount, status, time)
                cursor.execute(sql_parameterized_query, input_values)
                self.conn.commit()
                logging.info("Exited insert_transaction_details")
            except mysql.connector.Error as error:
                self.conn.rollback()
                raise DatabaseError(error)
            finally:
                self.close_connection()

    def change_password(self, password_1):
        # try:
            self.get_connection()
            cursor = self.conn.cursor()
            sql_parameterized_query = " update users set password_hash = %s where id = 18"            #hardcoded
            input_values = (password_1,)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
        # except mysql.connector.Error as error:
        #     self.conn.rollback()
        #     raise DatabaseError(error)

    def register_user(
            self,
            first_name,
            last_name,
            email,
            phone_number,
            password_hash,
            security_ans,
            security_question_id):
        try:
            self.get_connection()
            logging.info("Entered register_user")
            cursor = self.conn.cursor()
            sql_parameterized_query = """insert into users(first_name, last_name, email, phone_number,
            password_hash, security_ans, security_question_id) values(%s,%s,%s,%s,%s,%s,%s)"""
            input_values = (first_name, last_name, email, phone_number,
                            password_hash, security_ans, security_question_id)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
            logging.info("Exited register_user")
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def insert_payment(self, user_id, card_number, card_expiry_month, card_expiry_year, card_name):
        try:
            self.get_connection()
            logging.info("Entered insert_payment")
            cursor = self.conn.cursor()
            sql_parameterized_query = """insert into payments(user_id, card_number, card_expiry_month,
            card_expiry_year, card_name) values(%s,%s,%s,%s,%s)"""
            input_values = (user_id, card_number, card_expiry_month, card_expiry_year, card_name)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
            logging.info("Exited insert_payment")
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def get_payment_details(self, user_id):
        try:
            self.get_connection()
            logging.info("Entered get_payment_details")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select * from payments where user_id = %s"""
            input_values = (user_id,)
            cursor.execute(sql_parameterized_query, input_values)
            row_headers = [header[0] for header in cursor.description]
            result = cursor.fetchone()
            if result is None:
                return result
            json_data = [(dict(zip(row_headers, result)))]
            logging.info("Exited get_payment_details")
            return json_data[0]
        except mysql.connector.Error as error:
            logging.error("Error occurred at get_profile_details", error)
            raise DatabaseError("Unable to retrieve user details")
        finally:
            self.close_connection()

    def login_user(self, email, password_hash, auth_code):
        try:
            self.get_connection()
            logging.info("Entered login_user")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select first_name, last_name, 
            email, phone_number, security_question_id, security_ans, 
            id, invalid_password from users where email = %s and password_hash = %s"""
            input_values = (email, password_hash)
            cursor.execute(sql_parameterized_query, input_values)
            row_headers = [header[0] for header in cursor.description]
            result2 = cursor.fetchone()
            if result2 is None:
                return None

            sql_parameterized_query = """select expiry from auth_code where user_email = %s and authcode = %s"""
            input_values = (email,auth_code,)
            cursor.execute(sql_parameterized_query, input_values)
            result = cursor.fetchone()

            currentTime = (int(round(time.time() * 1000)))             
            print(currentTime)
            print(result[0])
            if currentTime <= int(result[0]):
                json_data = [(dict(zip(row_headers, result2)))]
                return json.dumps(json_data[0])
            else:
                logging.info("auth code expired")
                return -1

            logging.info("Exited get_profile_details")
        except mysql.connector.Error as error:
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def insert_ans(self, ans, questionID):
        try:
            self.get_connection()
            logging.info("Entered insertAns")
            cursor = self.conn.cursor()
            sql_parameterized_query = """insert into security_ans(answer, security_question_id) values(%s, %d)"""
            input_values = (ans, questionID)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
            logging.info("Exited insertAns")
            return cursor.lastrowid
        except:
            return "Database Error!"

    def get_bank_details(self, card_number):
        try:
            self.get_connection()
            logging.info("Entered get_bank_details")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select id,c_no,c_name,c_cvv,c_expiry_month,c_expiry_year
                                        ,c_limit from creditcardserver where c_no =%s"""
            input_values = []
            input_values.append(card_number)
            cursor.execute(sql_parameterized_query, input_values)

            result = cursor.fetchone()
            cursor.close()
            logging.info("Exited get_bank_details")
            return result
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def update_bank_balance(self, id, amount):
        try:
            self.get_connection()
            logging.info("Entered update_bank_balance")
            cursor = self.conn.cursor()
            sql_parameterized_query = """update creditcardserver set c_limit = %s where id = %s"""
            input_values = []
            input_values.append(amount)
            input_values.append(id)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
            cursor.close()
            logging.info("Exited update_bank_details")
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def get_id_from_email(self, email):
        try:
            self.get_connection()
            logging.info("Entered get_bank_details")
            cursor = self.conn.cursor()
            sql_parameterized_query = """select id from users where email =%s"""
            input_values = (email,)
            cursor.execute(sql_parameterized_query, input_values)
            result = cursor.fetchone()
            cursor.close()
            logging.info("Exited get_bank_details")
            return result
        except mysql.connector.Error as error:
            self.conn.rollback()
            raise DatabaseError(error)
        finally:
            self.close_connection()

    def invalid_login(self, email):
        try:
            self.get_connection()
            logging.info("Entered invalid_login")
            cursor = self.conn.cursor()
            sql_parameterized_query = """update users u1, users u2 set u1.invalid_password = u2.invalid_password + 1
            where u1.id = u2.id and u2.email = %s"""
            input_values = (email,)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
            cursor.close()
            logging.info("Exited invalid_login")
        except mysql.connector.Error as error:
            logging.error("Invalid email")
        finally:
            self.close_connection()

    def valid_login(self, email):
        try:
            self.get_connection()
            logging.info("Entered invalid_login")
            cursor = self.conn.cursor()
            sql_parameterized_query = """update users set invalid_password = 0 where email = %s"""
            input_values = (email,)
            cursor.execute(sql_parameterized_query, input_values)
            self.conn.commit()
            cursor.close()
            logging.info("Exited invalid_login")
        except mysql.connector.Error as error:
            logging.error("Invalid email")
        finally:
            self.close_connection()


    def send_email_auth_code(self, email):
            code = random.randint(100000, 999999)
            self.update_db_authcode(email, code)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(connection_email_details['email'], connection_email_details['password'])
            text_to_send = "Your login authentication code is "+ str(code) +"\nThe code will be valid for 24 hrs"
            msg = 'Subject: {}\n\n{}'.format("Authentication code", text_to_send)
            server.sendmail(connection_email_details['email'], email, msg)


    def update_db_authcode(self, email, gen_code):
            try:
                self.get_connection()
                cursor = self.conn.cursor()
                currentTime = (int(round(time.time() * 1000))) 
                print(currentTime)
                expiry  = currentTime + 86400000
                print(expiry)
                sql_parameterized_query = """select user_email from auth_code where user_email =%s"""
                input_values = (email,)
                cursor.execute(sql_parameterized_query, input_values)
                result = cursor.fetchone()

                if result is None:
                    sql_parameterized_query = """INSERT INTO auth_code(user_email, authcode, expiry) VALUES (%s, %s, %s)"""
                    input_values = (email, gen_code, expiry)
                    cursor.execute(sql_parameterized_query, input_values)
                else:
                    sql_parameterized_query = """UPDATE auth_code SET authcode=%s, expiry = %s  WHERE user_email = %s"""
                    input_values = (gen_code, expiry, email)
                    cursor.execute(sql_parameterized_query, input_values)
                
                self.conn.commit()
            except mysql.connector.Error as error:
                logging.error("Error occurred at get_profile_details", error)
                raise DatabaseError("Unable to insert data in auth code")
            finally:
                self.close_connection()

# --------------------Test---------------------------------

# user = users()
# data = {
# 	'first_name' : "Sahil",
# 	'last_name': "Sahil",
# 	'username':"sahil31",
# 	'email':"sahil.sahil@mavs.uta.edu",
# 	'phone_number':"682-561-7889",
# 	'password_hash': "ASDAdsakdamskm1331232100-mdasmdmska-dsa2312123",
# 	'security_question_id': 1,
# 	'security_ans_id': 1
# }
# print(user.insert(data))
# data = {
# 	'first_name' : "Sahil",
# 	'last_name': "Sahil"
# }
# print(user.get(data))
# del user

# ---------------------------------------------------------
