from flask import Flask,render_template,request,abort, jsonify
from Database import Database

from werkzeug.exceptions import HTTPException
import json
app = Flask(__name__)


global db
db=None

@app.route('/logout')
def logout():
    db=None
    return render_template('login.html',)


@app.errorhandler(404)
  
# inbuilt function which takes error as parameter
def not_found(e):
    return render_template('error.html')
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

@app.route('/')
def index():
    return render_template('login.html',)

@app.route('/login')
def login():
    return render_template('login.html',)

@app.route('/sign')
def sign():
    return render_template('signup.html',)

@app.route('/update',methods=['GET','POST'])
def update():
    if not db:
        return render_template('login.html',data="Something went wrong") 
    if request.method == 'POST':
        a=request.form['table']
        res=db.update(a)
    return challenges()

@app.route('/insert',methods=['GET','POST'])
def insert():
   
    if request.method == 'POST':
        a=request.form['user']
        b=request.form['pass1']
        
    db=Database(a)
    tmp=db.add_users(b)
    db=None
    
    
    return render_template('signup.html',data=tmp)


@app.route('/create',methods=['GET','POST'])
def create():
    global db
    if not db:
        return render_template('login.html',data="Something went wrong")
        
    tmp=None
    if request.method == 'POST':
     
        a=request.form['cname']
        a=a.strip()
        a=a.replace(' ','_')
      #  print(a)
        b=request.form['cdesc']
       # print(b)
        c=request.form['days']
       # print(a,b,c)
        if db:
            #print('indb')
            other=db.create_challenge(a,b,c)
            
        else:
            tmp="Wrong data"
    return render_template('login.html',data=tmp) if tmp else challenges()

@app.route('/open',methods=['GET','POST'])
def open():
    tmp="Something went wrong"
    if request.method == 'POST':
        a=request.form['user']
        b=request.form['pass']
        global db
        db=Database(a)
        tmp=db.authenticate(b)
   # print(tmp)
    return challenges() if tmp==1 else render_template('login.html',data=tmp) 


@app.route('/challenges')
def challenges():
    global db
    length,arr=0,[]
    if db:
        arr=db.fetch()
        length=len(arr)
    return render_template('box.html',len=length,arr=arr)




app.run(host='0.0.0.0', port=81)
