from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import pymysql
import traceback




app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '!ruzAtre4pum'
app.config['MYSQL_DB'] = 'html'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])

def index():


    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM a")
    data = cur.fetchall()


    return render_template('index.html', data=data)



@app.route('/add', methods=['GET', 'POST'])

def add():
    if request.method == "POST":
        details = request.form
        productname = details['productname']
        price = details['price']
        shopname = details['shopname']
        address = details['address']
        phonenumber = details['phonenumber']
        emailaddress = details['emailaddress']
        category = details['category']
        photolink = details['photolink']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO a(productname, price ,shopname, address, phonenumber, emailaddress, category, photolink) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (productname, price ,shopname, address, phonenumber, emailaddress, category, photolink))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add.html')




@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/regist')
def regist():
    return render_template('regist.html')


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/registuser')
def getRigistRequest():
    db = pymysql.connect("localhost","admin","!ruzAtre4pum","html" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句



    ab = request.args.get('user')
    cd = request.args.get('password')
    insert = ("INSERT INTO user (username,password) VALUES (%s, %s)")
    data = (ab, cd)


    try:
        cursor.execute(insert, data)
        db.commit()
        return render_template('login.html')
    except:
        traceback.print_exc()
        db.rollback()
        return '注册失败'
    db.close()


@app.route('/logina')
def getLoginRequest():
    db = pymysql.connect("localhost","admin","!ruzAtre4pum","html"  )
    cursor = db.cursor()



    ab = request.args.get('user')
    cd = request.args.get('password')
    set = (ab, cd)
    sql = "SELECT * FROM user WHERE username = %s AND password = %s"

    try:
        cursor.execute(sql, set)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return redirect(url_for('add'))
        else:
            return '用户名或密码不正确'

        db.commit()
    except:

        traceback.print_exc()
        db.rollback()
    
    db.close()




if __name__ == '__main__':
    app.debug = True
    app.run()
