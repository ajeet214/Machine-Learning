# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 20:27:39 2018

@author: ajeet
"""
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
import gunicorn

app = Flask(__name__)


@app.route("/")
def hello():
 return "Hoilaaaaaaaaa!"


@app.route('/predict', methods=['POST'])
def apicall():
    """API Call
    """
    try:
        test_json = request.get_json()
        val = []
        print(test_json)
        for dic in test_json:
           row = list()
           row.append(dic['experience'])
           val.append(row)
        #load model
        print(np.array(val))
        loaded_model = joblib.load('model/salary_exp_model.pkl')
        y_pred = loaded_model.predict(np.array(val))
        pred_dict = {}
        for i,pred in enumerate(y_pred):
           pred_dict['predicted_salary_'+str(i)] = int(pred)
        responses = jsonify(predictions=pred_dict)
        responses.status_code = 200
    except Exception as e:
        responses = jsonify(predictions={'error':'some error occured, please try again later'})
        responses.status_code = 404
        print ('error', e)
    return (responses)


if __name__ == "__main__":
    app.run() # remove debug = True, or set to False
