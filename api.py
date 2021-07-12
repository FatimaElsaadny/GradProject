from flask import Flask, request
import jsonpickle
#from business import sahabaAnalysis
import json
#from DataAccess.__Pycache__ import SahabaDA
import mysql.connector
import demo
conn = mysql.connector.connect(
               host="db4free.net",
               user="fatimaelsaadny",
               database="al_sahaba_db",
               password="123456789")
    

def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(
               host="db4free.net",
               user="fatimaelsaadny",
               database="al_sahaba_db",
               password="123456789")
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()

    
  

# Create flask app
app = Flask(__name__)

# API for TXTTS
@app.route('/sahabaById', methods=["GET"])
def sahabaById():
    
# 1  get id :
    id = request.args.get('personId')
#     id = request.args['personId']
    print(id)
    
# 2 check txt entity :   
    cursor = conn.cursor()
    sahaba = cursor.execute('SELECT Audio FROM personalities where personId=%s', [id])
    sahaba =cursor.fetchone()
    print("sahaba",sahaba[0])
    
   # if sahaba!= None:
    if None not in sahaba: 
        
        #1 retrive from database
        json_string = jsonpickle.encode(sahaba,unpicklable=False)
        response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json')
        print("response",response)
    else:
        #1 fetch txt from database
        txt=cursor.execute('SELECT txtNarration FROM personalities where personId=%s', [id])
        txt =cursor.fetchone()
        print("txt",txt[0].decode("utf-8"))
        
        #2 Run Method
        res=demo.final_func_forSpeech(txt[0].decode("utf-8"))
        #3 Store Ruselt
        ret = cursor.execute('UPDATE personalities SET Audio =%s where personId =%s',(res,id))
        print("ret",ret)
        
        #4 Retrive from database
        json_string = jsonpickle.encode(ret, unpicklable=False)
        response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json')
        print("ret",response)

        
        
        
    return response


if __name__ == '__main__':
    connect()
    app.run(host='127.0.0.1', port=5000)
