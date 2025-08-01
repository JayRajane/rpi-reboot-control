import os
import paramiko
from flask import Flask, jsonify, render_template_string, request, redirect, url_for
from flask_cors import CORS

# Flask setup
app = Flask(__name__)
CORS(app)

# Basic authentication
def check_auth():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'secret':
        return True
    return False

# Flask API and web GUI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Impulse Reboot Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { font-size: 24px; }
        button { font-size: 18px; padding: 15px 30px; margin: 10px; cursor: pointer;
                 background-color: #dc3545; color: white; border: none; border-radius: 5px; }
        button:hover { background-color: #c82333; }
        .warning { color: #dc3545; font-weight: bold; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Impulse Reboot Control</h1>
    <p class="warning">⚠️ Warning: This will immediately reboot Impulse!</p>
    <button onclick="rebootSystem()">Reboot Impulse</button>

    <script>
        async function rebootSystem() {
            if (confirm('Are you sure you want to reboot Impulse? This will disconnect all users.')) {
                try {
                    const response = await fetch('/api/reboot', { 
                        method: 'POST',
                        headers: {
                            'Authorization': 'Basic ' + btoa('admin:secret')
                        }
                    });
                    const data = await response.json();
                    if (data.success) {
                        alert('Reboot command sent! Impulse will restart shortly.');
                    } else {
                        alert('Error: ' + data.message);
                    }
                } catch (error) {
                    alert('Reboot initiated! Impulse is restarting...');
                }
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    if not check_auth():
        return 'Please provide username and password', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/reboot', methods=['POST'])
def reboot_system():
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    try:
        print("Reboot command received via web interface")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('impulse-reboot.duckdns.org', username='impulse', password='your-password', timeout=10)
        stdin, stdout, stderr = ssh.exec_command('sudo reboot')
        ssh.close()
        return jsonify({'success': True, 'message': 'Reboot initiated'})
    except Exception as e:
        print(f"Error during reboot: {e}")
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    try:
        print("Starting Impulse Web Reboot Control Server...")
        print("Access the web interface at: http://impulse.local:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
