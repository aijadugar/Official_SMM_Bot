from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
from flask_cors import CORS
from google.oauth2.service_account import Credentials
import gspread
import os
import json

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CORS(app)

creds_json = os.getenv('GOOGLE_CRED')
if not creds_json:
    raise Exception("GOOGLE_CRED is not loaded")

service_account_info = json.loads(creds_json)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
sheet = gspread.authorize(credentials).open_by_key('1JtYtzxObTCawJejMX0yxtDjOGiAN3bk2hnv-OA9vDX8').worksheet('Sheet4')

@app.route('/name', methods = ['POST'])
def name():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Name not found'}), 400
    
    sheet.append_row([name])

    return jsonify({'message': 'Name stored successfully'}), 200

@app.route('/phone')
def phone():
    return "function to store name on the google sheet"

@app.route('/email')
def email():
    return "function to store email on the google sheet"

@app.route('/address')
def address():
    return 'function to store address on the google sheet'

@app.route('/wanttostart')
def wanttostart():
    return "this function stores the when to start contract as options"

if __name__ == '__main__':
    app.run(debug=True)

