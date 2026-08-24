from flask import Flask, request, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/scan')
def scan():
    phone = request.args.get('phone', '')
    phone = phone.replace('+98', '0').replace('0098', '0')
    if phone.startswith('0'):
        phone = phone[1:]
    
    if not phone:
        return jsonify({'error': 'phone required'}), 400
    
    # ساخت پوشه bale_browser
    os.makedirs('browsers/bale_browser', exist_ok=True)
    
    # پاک کردن همه فایل‌های قفل
    for root, dirs, files in os.walk('browsers'):
        for file in files:
            if 'Singleton' in file:
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass
    
    result = subprocess.run(
        [sys.executable, 'main.py', phone],
        capture_output=True,
        text=True
    )
    
    return jsonify({
        'phone': phone,
        'output': result.stdout,
        'error': result.stderr
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
