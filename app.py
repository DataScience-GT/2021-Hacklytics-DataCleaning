from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template, redirect, send_file
import pandas as pd
import werkzeug

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('clean.html')

@app.route('/clean', methods=['POST'])
def create_task():
    nullValue = request.form.get('nullValues')
    interpolation = request.form.get('interpolation')
    file = request.files['file']

    df = pd.read_csv(file)
    if nullValue:
      df.dropna(inplace=True)

    df.interpolate(method=interpolation, axis=0, inplace=True)
    df.to_csv('./data.csv')
    
    return send_file('./data.csv',
                     mimetype='text/csv',
                     attachment_filename='data.csv',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
