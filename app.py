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
    
    # ساخت پوشه خالی bale_browser
    os.makedirs('browsers/bale_browser', exist_ok=True)
    
    # پاک کردن SingletonLock ها
    lock_files = [
        'browsers/splus_browser/SingletonLock',
        'browsers/eitaa_browser/SingletonLock',
        'browsers/shad_browser/SingletonLock',
        'browsers/igap_browser/SingletonLock',
        'browsers/bale_browser/SingletonLock',
        'browsers/rubika_browser/SingletonLock',
    ]
    
    for lock_file in lock_files:
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
            except:
                pass
    
    # پاک کردن فایل‌های قفل دیگر
    for root, dirs, files in os.walk('browsers'):
        for file in files:
            if file == 'SingletonLock' or file == 'SingletonCookie' or file == 'SingletonSocket':
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass
    
    result = subprocess.run(
        [sys.executable, 'main.py', phone],
        capture_output=True,
        text=True,
        timeout=600
    )
    
    return jsonify({
        'phone': phone,
        'output': result.stdout,
        'error': result.stderr
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
