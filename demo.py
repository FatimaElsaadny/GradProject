#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example code using Shakkala library
"""
import os
from gtts import gTTS
from Shakkala import Shakkala
from flask import Flask, request
import jsonpickle
#from business import sahabaAnalysis
import json
#from DataAccess.__Pycache__ import SahabaDA
import mysql.connector




def startmodel():
    if __name__ == "__main__":

        folder_location = './'
        global sh
        sh = Shakkala(folder_location, version=3)
        global model
        model, graph = sh.get_model()
    
    


#=============================================
#extract text from text file
def extractTextFromFile(path):
    
    f = open(path,'r',  encoding='utf-8')
    filetext = str(f.read())
    return filetext

#=================================================
#text partition
def txt_partitionAndTashkeel(text):
    allTextAfterTashkeel= ""
    part = ""
    startmodel()
    for i in range(0, len(text),300):
        if i+300 <= len(text):
            part = text[i:i+300]
            allTextAfterTashkeel = allTextAfterTashkeel +tashkeel(part)
        else:
            part = text[i:len(text)]
            allTextAfterTashkeel = allTextAfterTashkeel +tashkeel(part)
            
    return allTextAfterTashkeel
#=============================================
#tashkeel text
def tashkeel(textPart):
    # prepare input
    global sh
    input_int = sh.prepare_input(textPart)
    # with graph.as_default():
    logits = model.predict(input_int)[0]
    predicted_harakat = sh.logits_to_text(logits)
    
    partAfterTashkeel = sh.get_final_text(textPart, predicted_harakat)
    return partAfterTashkeel

#===================================================
#convert text to speech and play it
def produce_audio(text,name):

    audioName = name
    tts = gTTS(text, lang= 'ar' ,lang_check=(True) ,slow=(False))
    tts.save(audioName)
    return audioName

#====================================================

def final_func_forSpeech(filetxt,name):
   
    finalTextoutput = txt_partitionAndTashkeel(filetxt)
    print(finalTextoutput)
    audioname = produce_audio(finalTextoutput,name)
    return audioname
#=====================================================
#calling final functi





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

    audioname = "audio"+id+".mp3"
    print("person name: ", audioname)
    
    selectedAudio = cursor.execute('SELECT Audio FROM personalities where personId=%s', [id])
    selectedAudio =cursor.fetchone()
    mselectedAudio = selectedAudio[0]
    print("selectedAudio: ",mselectedAudio)
    
   # if sahaba!= None:
    if None not in selectedAudio: 
        print("Audio already exist in db")
        
        os.system(mselectedAudio.decode("utf-8"))                                    
        print("played")
        #1 retrive from database
        json_string = jsonpickle.encode(selectedAudio[0].decode("utf-8"),unpicklable=False)
        response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json')
        print("response",response)
    else:
        #1 fetch txt from database
        txt=cursor.execute('SELECT txtNarration FROM personalities where personId=%s', [id])
        txt =cursor.fetchone()
        txt = txt[0].decode("utf-8")
        print("txt",txt)
        
        #2 Run Method
        res=final_func_forSpeech(txt,audioname)
        print("audio finish")
        #3 Store Ruselt


        ret = cursor.execute('UPDATE personalities SET Audio = %s where personId =%s',(audioname,id))
        conn.commit()
        print("updated successfully")
        
        
        audio=cursor.execute('SELECT Audio FROM personalities where personId=%s',[id])
        audio = cursor.fetchone()
        audio = audio[0].decode("utf-8")            
        print("ret",audio)
        
        
        os.system(audio)
        
        #4 Retrive from database
        json_string = jsonpickle.encode(audio, unpicklable=False)
        response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json')
        print("response",response)
       
    return response



if __name__ == '__main__':
    connect()
    app.run(host='127.0.0.1', port=5000)
