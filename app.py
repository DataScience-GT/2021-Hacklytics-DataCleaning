from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template, redirect, send_file
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('clean.html')

@app.route('/clean', methods=['POST'])
def clean_file():
    nullValue = request.form.get('nullValues')
    interpolation = request.form.get('interpolation')
    file = request.files['file']

    mimetype = file.content_type
    
    if mimetype == 'text/csv' or mimetype == 'application/vnd.ms-excel':
      df = pd.read_csv(file)
    else:
      df = pd.read_excel(file)

    if nullValue:
      df.dropna(inplace=True)
    
    if interpolation == 'linear':
      df.interpolate(method='linear', axis=0, inplace=True)
    else:
      df.interpolate(method=interpolation, order=2, axis=0, inplace=True)
      
    redirect('http://localhost:5000')
    if mimetype == 'text/csv' or mimetype == 'application/vnd.ms-excel':
      df.to_csv('./data.csv')
      return send_file('./data.csv',
                     mimetype='text/csv',
                     attachment_filename='data.csv',
                     as_attachment=True)
    else:
      df.to_excel('./data.xlsx')
      return send_file('./data.xlsx',
                     mimetype='text/xlsx',
                     attachment_filename='data.xlsx',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
