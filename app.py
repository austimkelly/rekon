from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# For serving static files
app.config['STATIC_FOLDER'] = 'static'

scanning_in_progress = False
active_process = None

@app.route('/run_scan', methods=['POST'])
def run_scan():
    global scanning_in_progress, active_process

    print("Starting app scan...")

    # Set the flag to indicate scanning is in progress
    scanning_in_progress = True

    try:
        # Run your Python script as a subprocess
        active_process = subprocess.Popen(['python3', 'rekon.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read the output of the subprocess line by line
        for line in iter(active_process.stdout.readline, ''):
            socketio.emit('scan_update', {'data': line.strip()})
            time.sleep(0.1)  # Add a slight delay to avoid flooding the client with updates

        # Wait for the subprocess to finish and get the return code
        return_code = active_process.wait()

        # Emit the final output with the return code
        socketio.emit('scan_update', {'data': f"Scan completed with code {return_code}\n"})
        socketio.emit('scan_complete')

    except Exception as e:
        print(f"Error during scan: {e}")

    finally:
        # Reset the scanning status
        scanning_in_progress = False
        result = "Scan completed."
        socketio.emit('scan_complete')
        return result

    print("Finished app scan...")

@app.route('/')
def index():
    return render_template('index_socketio.html', scanning=scanning_in_progress)

@socketio.on('run_scan')
def handle_run_scan():
    global active_process

    if not scanning_in_progress:
        # Start the scan in a separate thread to avoid blocking the SocketIO event loop
        threading.Thread(target=run_scan).start()

@socketio.on('cancel_scan')
def handle_cancel_scan():
    global scanning_in_progress, active_process

    if active_process:
        # Terminate the active scan process
        active_process.terminate()

    # Reset the scanning status
    scanning_in_progress = False

@socketio.on('reset')
def handle_reset():
    global scanning_in_progress

    # Reset the scanning status
    scanning_in_progress = False

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
