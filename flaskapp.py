from flask import Flask, render_template, send_from_directory, redirect, request, session, url_for, Response, \
    make_response
from werkzeug.utils import secure_filename
import mysql.connector, hashlib, os
from mysql.connector import errorcode
import pymemcache
from pymemcache.client.base import Client
import base64
import datetime
from datetime import tzinfo

app = Flask(__name__)
app.secret_key = "RANDOM"

host = ''
port = 3306
dbusername =''
dbpassword =''
dbname =''

@app.route('/')
def home():
    return render_template('register.html')



@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        return render_template('upload.html', username=session['username'])
    if request.method == 'POST':
        db = mysql.connector.connect(host=host, user=dbusername, password=dbpassword, database=dbname, port=port)
        cursor = db.cursor(buffered=True)

        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            return render_template('register.html')

        sql = "select username from users where username='"+username+"'"
        cursor.execute(sql)
        if cursor.rowcount == 1:
            return render_template('register.html')
        sql = "insert into users (username, password) values ('" + username + "','" + hashlib.md5(password).hexdigest() + "')"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        return render_template('login.html')
    else:
        return render_template('register.html')



@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template('upload.html', username=session['username'])
    if request.method == 'POST':
        db = mysql.connector.connect(host=host, user=dbusername, password=dbpassword, database=dbname, port=port)
        cursor = db.cursor()

        username = request.form['username']
        print username


        #print hashlib.md5(password).hexdigest()
        sql = "select username from users where username = '"+username+"'"
        print sql
        cursor.execute(sql)
        #print "excecute 1"
        print cursor.rowcount
        if cursor.rowcount < 1:
            results = cursor.fetchall()
            for rows in results:
                print rows
                session['username'] = username
                return render_template('upload.html', username=session['username'])
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

UploadPath ="/home/ubuntu/Uploads"


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        db = mysql.connector.connect(host=host, user=dbusername, password=dbpassword, database=dbname, port=port)
        cursor = db.cursor(buffered=True)

        file = request.files['file']
        filename = secure_filename(file.filename)
        title = file.filename

        rating = request.form['likes']

        file.save(os.path.join(UploadPath, filename))
        fileCreatedTime = os.stat(UploadPath + '/' + filename).st_mtime
        fileCreatedTime = str(datetime.datetime.fromtimestamp(fileCreatedTime))

        with open(UploadPath+ '/'+filename, 'rb') as sample_file:
            file_contents = base64.b64encode(sample_file.read())

        sql = "select username from photos where username = '" +session['username']+ "'"

        #print sql
        cursor.execute(sql)
        print cursor.rowcount
        if cursor.rowcount > 0:
            return '<h4>File '+title+'already exists</h4>'

        sql = "insert into photos (username,pic_name,pic_time) values ('" +session['username']+ "','"+title+ "','"+fileCreatedTime+"')"
        print sql
        cursor.execute(sql)
        db.commit()
        cursor.close()
        messageText = "Image Uploaded Successfully"
        return render_template('upload.html', messageText=messageText)
    else:
        return render_template('upload.html', message="Upload Again")


@app.route('/listPhotos', methods=['POST', 'GET'])
def listPhotos():
    if 'username' not in session:
        return render_template('register.html')
    if request.method == "GET":
        db = mysql.connector.connect(host=host, user=dbusername, password=dbpassword, database=dbname, port=port)
        cursor2 = db.cursor(buffered=True)
        query1 = "select username, pic_name, pic_time from photos where username='"+session['username']+"'"
        cursor2.execute(query1)
        results = cursor2.fetchall()
        photolist = []
        for r in results:
            photolist.append([r[0],r[1],r[2]])
        cursor2.close()
        return render_template('listPhotos.html', images=photolist)
    else:
        return "try again!"

if __name__ == '__main__':
  app.run()



