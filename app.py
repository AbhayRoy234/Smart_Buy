from flask import Flask, request, jsonify
import re
from common import dbHandle

app = Flask(__name__)

@app.route('/login', methods=["POST"])
def login():
    form_data = request.form.to_dict()
    email = form_data['email']
    passwd = form_data['pass']
    emailexp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(emailexp, email):
        return "Enter a valid email"
    elif passwd == '':
        return "Enter your password"
    success = dbHandle.login(email, passwd)
    print(success)
    if success == -1:
        print("Email id not found")
        return "email id not found please register"
    elif success == 0:
        print("Incorrect password")
        return "incorrect password"
    elif success == 1:
        print("Login Success")
        # session['email'] = email
        user_info = dbHandle.get_userdetails(email)
        userid = str(user_info['userid'])
        products = dbHandle.get_products(userid)
        notifs = dbHandle.notify(products)

        return jsonify(success=1, user_info=user_info, products_info=products, notifs=notifs)
    else:
        return "logged in"

@app.route('/register', methods=["POST"])
def register():
    form_data = request.form.to_dict()
    name = form_data['name']
    passwd = form_data['pass']
    email = form_data['email']
    passwdchk = form_data['passcheck']
    emailexp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    print(name, email, passwd)
    if name == '':
        return "Please enter your name"
    elif not re.match(emailexp,email):
        return "Please enter a valid email"
    elif passwd == '':
        return "Please enter a password"
    elif passwdchk == '':
        return "Please enter confirm password"
    elif passwd != passwdchk:
        return "Password and confirm password do not match, Please re-enter"



    success = dbHandle.user_registration(name, email, passwd)

    # if success == 1:
    #     print("new user registered")
    #     session['email'] = email
    #     return "success"

    if success == 1:
        # session[email] = email
        print("success")
        user_info = dbHandle.get_userdetails(email)
        products = []
        notifs = []
        return jsonify(success=1, user_info=user_info, products_info=products, notifs=notifs)

    elif success == 0:
        return "Email already exists, Please login"

@app.route('/dashboard', methods=["POST"])
def dashboard():
    data = request.form.to_dict()
    userid = data['userid']
    print(data)
    products = dbHandle.get_products(userid)
    notifs = dbHandle.notify(products)
    print(products)
    print(notifs)
    return jsonify(success=1, user_info=data, products_info=products, notifs=notifs)

@app.route('/addproduct', methods=["POST"])
def addproduct():
    data = request.form.to_dict()
    print(data)
    url = data['url']
    userid = int(data['userid'])
    addproduct = dbHandle.add_product(url,url,userid)
    del data['url']
    products = dbHandle.get_products(str(userid))
    notifs = dbHandle.notify(products)
    print(products)
    return jsonify(addproduct=addproduct, success=1,user_info=data, products_info=products, notifs=notifs)


if __name__ == '__main__':
    app.run()
