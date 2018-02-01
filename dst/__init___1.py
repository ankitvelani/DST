from flask import Flask
from flask import Response
from flask import render_template
from flask import request
import json
import numpy as np
import os
import pandas as pd
from werkzeug import secure_filename

UPLOAD_FOLDER = './input/'
INPUT_DIR = 'input/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


 

@app.route('/', methods=['GET', 'POST'])
def index():
    N = 10 # No Of Records
    requestData = request.form
    filename = requestData['filename']
    pd.data = pd.read_csv(INPUT_DIR + filename)
    sample = pd.data.head(N).to_json(orient='records')
    return sample

@app.route('/Field/Get', methods=['GET', 'POST'])
def getField():
    if request.method == 'POST':
        filename = "test.csv" #request.form.get('filename')
        if filename is None:
            return Response(response=json.dumps({"result":[{'code':400, 'message':'File name is missing'}]}), status=400, mimetype="application/json")	
        else:
            pd.data = pd.read_csv(INPUT_DIR + filename)
            pd.Structure = pd.DataFrame(pd.data.dtypes).reset_index()    
            pd.Structure.columns = [['Fields', 'DataTypes']]    
            pd.Structure['Fields'] = pd.Structure.Fields.astype(str)
            pd.Structure['DataTypes'] = pd.Structure.DataTypes.astype(str)
	
            ret = pd.Structure.to_json(orient='records')
            return Response(response=ret, status=200, mimetype="application/json")
		
			
    else:
        return Response(response=json.dumps({"result":[{'code':400, 'message':'Method is not supported'}]}), status=400, mimetype="application/json")

@app.route('/File/Upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
    	file = request.files['file']
    	filename = secure_filename(file.filename)
    	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    	return Response(response=json.dumps({"result": [{'code':200, 'message':'FileUploaded'}]}),
                        status=200,
                        mimetype="application/json")
    	
    
    if request.method == 'GET':
    	return json.dumps({"result": [{'code':404, 'message':'Method is not supporting '}]})


@app.route('/File/List')
def list_files():
    if request.method == 'GET':
        files = os.listdir('input/')
        l = [{'file':w, 'size':os.stat(INPUT_DIR + w).st_size / (1024 * 1024), "unit":"MB"} for w in os.listdir(INPUT_DIR)]
        print(l)
        return Response(response=json.dumps({"result": l, 'code':200, 'message':'Success'}),
                        status=200,
                        mimetype="application/json")
    	

if __name__=='__main__':
    app.run(debug=True)
