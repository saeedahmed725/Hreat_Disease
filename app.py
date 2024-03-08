from flask import Flask, render_template, url_for, request
from functions import m1 , m2
# import pandas as pd

app = Flask(__name__)

features = ["age","sex","cp","trestbps","chol","fbs","restecg", "thalach", "exang", "oldpeak","slope","ca","thal","target"
,'ejection_fraction','serum_creatinine','time','creatinine_phosphokinase', 'serum_sodium','platelets','high_blood_pressure', 'smoking', 'diabetes']

f=['ejection_fraction','serum_creatinine','time','creatinine_phosphokinase', 'serum_sodium','platelets','high_blood_pressure', 'smoking', 'diabetes']


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result1", methods=['POST', 'GET'])
def result1():
    # output = request.form
    output = request.get_json()
    print(output)
    r = m1(output)

    if r == 0:
        r = "no disease"
    else:
        r = "has a disease"
    return r
    # return render_template("index.html", ftest=r)


@app.route("/result2", methods=['POST', 'GET'])
def result2():

    # output = request.form
    output = request.get_json()
    r = m2(output)

    if( r == 0):
        r = "has no Hreat failur"
    else:
        r = "May has Hreat failur"
    return r
    # return render_template("index.html" ,stest = r)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
