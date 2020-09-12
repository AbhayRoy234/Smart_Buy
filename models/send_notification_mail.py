import smtplib
from common.dbHandle import get_products
from common.dbHandle import connect


def sending_mail():
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("select userid from users_info")
    userlist = mycursor.fetchall()
    print(userlist)
    for j in userlist:
        # print(j[0])
        productlist = get_products(str(j[0]))
        le = len(productlist)
        for i in range(le):
            price_updated = productlist[i]['price_update']
            price_init = productlist[i]['price_init']
            if price_init > price_updated:
                mycursor.execute("select emailid from users_info where userid = \"" + str(j[0]) + "\"")
                email_info = mycursor.fetchall()
                for mailid in email_info:
                    # print(mailid)
                    # print(productlist[i])
                    sendmail(mailid[0], productlist[i])


def sendmail(username: str, productInfo: dict):
    content = f"The price of the product {productInfo['product_name']}.. has dropped to Rs.{int(productInfo['price_update'])}\n " \
              f"follow the link to buy now\n{productInfo['aff_url']}"
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()  # to check  the mail domain
    mail.starttls()  # to start transport layer security
    mail.login('smartbuyaass@gmail.com', '*******')
    header = 'T0:' + 'username' + '\n' + 'From :' + 'smartbuyaass@gmail.com' + '\n' + 'Subject :Testing \n'
    content = header + content
    mail.sendmail('smartbuyaass@gmail.com', username, content)
    mail.close()

sending_mail()