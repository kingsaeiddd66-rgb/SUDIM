# app.py - API برای SUDIM
from flask import Flask, request, jsonify
import subprocess
import sys

app = Flask(__name__)

@app.route('/scan')
def scan():
    phone = request.args.get('phone', '')
    
    if not phone:
        return jsonify({'error': 'phone required'}), 400
    
    # اجرای SUDIM
    result = subprocess.run(
        [sys.executable, 'main.py', phone],
        capture_output=True,
        text=True,
        timeout=300
    )
    
    return jsonify({
        'phone': phone,
        'output': result.stdout,
        'error': result.stderr
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
