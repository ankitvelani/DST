from flask import Flask, render_template, request
from werkzeug import secure_filename
import json , requests
import pandas as pd
import numpy as np 
app=Flask(__name__)

def GetCallURL(URL,header):
    Endpoint=URL
    headers=header
    response=""
    try:
        response=requests.get(Endpoint,headers=headers)
        response=response.content
    except :
        response="Error at API Call"

    return response

@app.route('/')
def index():
    header=""
    data = {'filename':'test.csv'}
    response = requests.post('http://127.0.0.1:5000/Field/Get', json=data)
    data['FieldMetadata']=pd.read_json(response.text, orient='records')
    return render_template('blank.html',data=data)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader',methods = ['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		return ("Uploader")
	else:
		return("Else Upload")

if __name__=='__main__':
    app.run(debug=True,port=8088)
