import mysql.connector
import bcrypt
from models import getting_the_price

def connect():
    try :
        mydb = mysql.connector.connect(
            host='us-cdbr-east-06.cleardb.net',
            user='b277c5bb846d1b',
            password='2341e971',
            database='heroku_ba21d3848c7d868',
        )
    except :
        connect()
    return mydb
# mysql://b277c5bb846d1b:2341e971@us-cdbr-east-06.cleardb.net/heroku_ba21d3848c7d868?reconnect=true

def user_registration(username: str, emailid: str, passwd: str):
    mydb = connect()
    mycursor = mydb.cursor()
    hassedPasswd = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())
    try:
        insertFn = "INSERT INTO users_info (username,emailid,passwd) VALUES (%s, %s, %s)"
        registration_info = (username, emailid, hassedPasswd)
        mycursor.execute(insertFn, registration_info)
        mydb.commit()
        return 1
    except :
        return 0 #email exists


def login(emailid: str, passwd: str):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT passwd from users_info where emailid = \""+emailid+"\"")
    fetched_list = mycursor.fetchall()
    if(len(fetched_list)==0):
        return -1   #email id not found

    else:
        hassedPasswd = fetched_list[0][0]
        if bcrypt.checkpw(passwd.encode("utf-8"), hassedPasswd.encode("utf-8")):
            return 1  #login success
        else:
            return 0  #incorrect password


def add_product(url: str,aff_url:str, userid: int):
    try:
        price, name = getting_the_price.get_price_name(url)
    except :
        return 0  #price could not be fetched for item (site is still not added)
    mydb = connect()
    mycursor = mydb.cursor()
    try:
        # if product don't exists in the database
        insertFn = "INSERT INTO product_info (url,aff_url,price_init,name) VALUES (%s, %s, %s, %s)"
        product_info = (url, aff_url, price, name)
        mycursor.execute(insertFn, product_info)
        mydb.commit()
    except :
        # if the product is in database
        pass
    mycursor.execute("SELECT product_id from product_info where url = \"" + url + "\"")
    product_id = int(mycursor.fetchall()[0][0])
    #mapping product with user id
    insertFn = "INSERT INTO mapping (userid, product_id) VALUES (%s, %s)"
    mapping_info = (userid, product_id)
    mycursor.execute(insertFn, mapping_info)
    mydb.commit()
    return 1

def get_products(userid: str):
    mydb = connect()
    mycursor = mydb.cursor()
    productlist = []
    mycursor.execute("SELECT product_id from mapping where userid = \"" + userid + "\"")
    fetched_list = mycursor.fetchall()
    le = len(fetched_list)
    if le == 0:
        return productlist  #no products register
    else:
        for i in range(le):
            mycursor.execute("select * from product_info where product_id = "+str(fetched_list[i][0]))
            list = mycursor.fetchall()
            if list[0][4] is None:
                tempdict = {"product_id": list[0][0],
                            "aff_url": list[0][2],
                            "price_init": list[0][3],
                            "price_update": list[0][3],
                            "product_name": list[0][5][0:20]}
            else:
                tempdict = {"product_id": list[0][0],
                            "aff_url": list[0][2],
                            "price_init": list[0][3],
                            "price_update": list[0][4],
                            "product_name": list[0][5][0:20]}
            productlist.append(tempdict)
        return productlist

def notify(products) :
    notifylist = []
    le = len(products)
    for i in range(le):
        price_updated = products[i]['price_update']
        price_init = products[i]['price_init']
        if price_init > price_updated:
            tempdict = products[i]
            notifylist.append(tempdict)
    return notifylist


def get_userdetails(email: str):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from users_info where emailid = \"" + email + "\"")
    fetched_list = mycursor.fetchall()
    le = len(fetched_list)
    if le == 0:
        return -1  # no such user found
    else:
        user_info= {"userid": fetched_list[0][0],
                    "username": fetched_list[0][1],
                    "email": fetched_list[0][2]
                    }
        return user_info

# url="https://www.amazon.in/Lipton-Pure-Light-Green-Pieces/dp/B01A6S21V6/ref=lp_21246951031_1_3?srs=21246951031&ie=UTF8&qid=1586463241&sr=8-3"
# add_product(url,url,2)


# success = user_registration("Amit kumar","amitkr0921@gmail.com","Amitkr943")
# print(success)

# product=get_products("1")
# print(product)
#
# user_info = get_userdetails("amitkr0921@gmail.com")
# print(user_info)


