from flask import Flask, render_template, request, jsonify
import pandas as pd
import datetime

Validator = Flask(__name__)
DB_FILE = 'master_event_db.csv'

# Load DB into memory
df = pd.read_csv(DB_FILE)
df.columns = df.columns.str.strip()
if 'UniqueID' not in df.columns:
    print("ERROR: 'UniqueID' column missing from CSV.")
else:
    df.set_index('UniqueID', drop=False, inplace=True)

@Validator.route('/')
def index():
    return render_template('scanner.html')

@Validator.route('/validate', methods=['POST'])
def validate():
    data = request.json
    scanned_id = data.get('qr_data')
    
    if scanned_id not in df.index:
        return jsonify({"status": "error", "message": "INVALID TICKET", "color": "red"})

    person = df.loc[scanned_id]
    
    # Check boolean value safely
    if str(person['CheckedIn']).lower() == 'true':
        msg = f"ALREADY USED: {person['FirstName']}"
        return jsonify({"status": "warning", "message": msg, "color": "orange"})

    df.at[scanned_id, 'CheckedIn'] = True
    df.to_csv(DB_FILE, index=False)
    
    msg = f"ACCESS GRANTED: {person['FirstName']} {person['LastName']}"
    return jsonify({"status": "success", "message": msg, "color": "green"})

if __name__ == '__main__':
    # Standard Flask run (Gunicorn ignores this block anyway)
    Validator.run(debug=True, host='0.0.0.0', port=5001)
