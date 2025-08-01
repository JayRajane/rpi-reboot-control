# Impulse Reboot Control
A Flask web app to remotely reboot a Raspberry Pi named "impulse" via a web interface.

## Setup
1. Clone the repo: `git clone https://github.com/JayRajane/rpi-reboot-control.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

## Usage
Access at `http://impulse.local:5000` (local network) or `http://<impulse-ip>:5000` to trigger a reboot.
