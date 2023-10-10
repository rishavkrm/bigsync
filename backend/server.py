from flask import Flask, request, render_template,jsonify
from flask_cors import CORS
import pandas as pd
from algorithms.main import FaultDetection 
from algorithms.main import EventClassification
from algorithms.main2 import FaultDetectionV1 
from algorithms.main2 import EventClassificationV1
import json


app = Flask(__name__)
# Allow requests from all origins
CORS(app)
@app.errorhandler(Exception)
def handle_generic_error(e):
    # Log the error for debugging purposes
    app.logger.error(str(e))
    
    # Return a generic error response with a 500 status code
    return jsonify({'error': 'An unexpected error occurred'}), 500
# 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/v1/detect-event', methods=['POST'])

# ---------------------version-1 -------------------------# 
 
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "File not provided"}), 400
    file = request.files['file']
    windowSize = float(request.form['windowSize']) if 'windowSize' in request.form else None
    sd_th = float(request.form['sd_th']) if 'sd_th' in request.form else None
    if file.filename == '':
        return jsonify({"error": "File not found"}), 400
    if file:
        faultDetection = FaultDetectionV1()
        res = faultDetection.getFault(file,windowSize,sd_th)
        # res = algorithm(file,windowSize,0.025)
        if(res):
            data_freq = res[0].tolist()
            data_rocof = res[1].tolist()
            data_time = res[2].tolist()
            return {"fault":True,"freq":data_freq, "time":data_time,"rocof":data_rocof}
        else:
            return {"fault":False}
        
@app.route('/v1/classify-event',methods=['POST'])
def classifyEvent():
    if 'file' not in request.files:
        return jsonify({"error": "File not provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "File not found"}), 400
    if file:
        eventClasify =  EventClassificationV1(file)
        return eventClasify.classifyEvents()


# -------------------------------- version-2 -----------------------------#

@app.route('/v2/classify-event',methods=['POST'])
def classifyEventData():
    body = request.get_json()
    if(not(body or body['time'] or body['data'])):
        return jsonify({"error": "Bad request from client!!!"}), 400
    time = body['time']
    data = body['data']
    threshold_values = body['thresholdValues']
    print(threshold_values)
    
    # print(data)
    if time and data:
        eventClasify =  EventClassification([body,time,threshold_values])
        return eventClasify.classifyEvents()

@app.route('/v2/detect-event',methods=['POST'])
def detectEvent():
    body = request.get_json()
    if(not(body or body['time'] or body['data'])):
        return jsonify({"error": "Bad request from client!!!"}), 400
    time = body['time']
    data = body['data']
    windowSize = body['windowSize']
    sd_th = body['sd_th']
    faultDetection = FaultDetection()
    res = faultDetection.getFault([data,time],float(windowSize),float(sd_th))

    if(res):
        data_freq = res[0].tolist()
        data_rocof = res[1].tolist()
        data_time = res[2].tolist()
        return {"fault":True,"freq":data_freq, "time":data_time,"rocof":data_rocof}
    else:
        return {"fault":False}
    
@app.route('/v2/detect-islanding-event',methods=['POST'])
def detectIslandingEvent():
    body = request.get_json()
    if(not(body or body['time'] or body['data'])):
        return jsonify({"error": "Bad request from client!!!"}), 400
    time = body['time']
    datas = body['data']
    threshold_values = body['thresholdValues']
    if time and datas:
        eventClasify =  EventClassification([body,time,threshold_values])
        res = eventClasify.islandingEvent([time,datas])
        return res

if __name__ == '__main__':
    app.run(port=5000)
