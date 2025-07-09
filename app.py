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

@app.route('/name', methods=['POST'])
def name():
    global last_row_index
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Name not found'}), 400

    # Add name in column A, create new row
    sheet.append_row([name])
    last_row_index = len(sheet.get_all_values())  # Store current row index

    return jsonify({'message': 'Name stored successfully'}), 200


@app.route('/phone', methods=['POST'])
def phone():
    global last_row_index
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        return jsonify({'error': 'Phone not found'}), 400

    if last_row_index is None:
        return jsonify({'error': 'No name record to associate with'}), 400

    # Update phone in column B of last_row_index
    sheet.update_cell(last_row_index, 2, phone)  # Column 2 = 'B'

    return jsonify({'message': 'Phone stored successfully'}), 200

@app.route('/email', methods=['POST'])
def email():
    global last_row_index
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email not found'}), 400

    if last_row_index is None:
        return jsonify({'error': 'No record to associate email with'}), 400

    # Column 3 = 'C'
    sheet.update_cell(last_row_index, 3, email)

    return jsonify({'message': 'Email stored successfully'}), 200


@app.route('/pincode', methods=['POST'])
def pincode():
    global last_row_index
    data = request.get_json()
    pincode = data.get('pincode')

    if not pincode:
        return jsonify({'error': 'Pincode not found'}), 400

    if last_row_index is None:
        return jsonify({'error': 'No record to associate pincode with'}), 400

    # Column 4 = 'D'
    sheet.update_cell(last_row_index, 4, pincode)

    return jsonify({'message': 'Pincode stored successfully'}), 200


@app.route('/start-time', methods=['POST'])
def startTime():
    global last_row_index
    data = request.get_json()
    start_choice = data.get('start_choice')

    if not start_choice:
        return jsonify({'error': 'Start choice not found'}), 400

    if last_row_index is None:
        return jsonify({'error': 'No record associate start choice with'}), 400
    
    sheet.update_cell(last_row_index, 5, start_choice)

    return jsonify({'message': 'Start choice stored successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

