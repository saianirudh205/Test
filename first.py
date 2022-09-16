from flask import Flask,render_template,request
import Database
import json
app = Flask(__name__)

db=None
@app.route('/')
def index():
    return render_template('login.html',)

@app.route('/open',methods=['GET','POST'])
def open():
    print('here i am')
    if request.method == 'POST':
        a=request.form['text']
        b=request.form['pass']
    db=Database(a)
    return challenges()


@app.route('/challenges')
def challenges():
    length,arr=0,[]
    if db:
        arr=db.fetch()
        length=len(arr)
    length,arr=0,[]  
    return render_template('box.html',length=length,data=arr)


@app.route('/test', methods=['POST','GET'])
def test():
    print('here am iiiii')
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    return "<h1>-----------</h1>"

app.run(host='0.0.0.0', port=81)
