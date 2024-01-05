from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from datetime import datetime
import logging
import re
import signal
import sys

def graceful_shutdown(sig, frame):
    logging.info('Shut down gracefully')
    sys.exit(0)
# Ctrl-C
signal.signal(signal.SIGINT, graceful_shutdown)
# kill command
signal.signal(signal.SIGTERM, graceful_shutdown)

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app,
    default_limits=["200 per day", "120 per hour"]
)

logging.basicConfig(level=logging.ERROR,
                    filename='errorlog.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
# verifying if server is working

@app.route('/')
def home():
    return 'Welcome to the Contact Form Server!'

# handling submission
@app.route('/send', methods=['POST'])

@limiter.limit("2/minute")

def send_email():
    try:
        data = request.json

        def validate_name(name):
            return re.match(r'^[a-zA-Z\s]{2,50}$', name) is not None

        def validate_email(email):
            return re.match(r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$', email) is not None
        
        def validate_message(message):
            return len(message) > 0 and len(message) < 500
        
        if not validate_name(data.get('name', '')):
            return "Invalid name", 400
        if not validate_email(data.get('email', '')):
            return "Invalid email", 400
        if not validate_message(data.get('message', '')):
            return "Invalid message", 400

        def sanitize(input_string):
            return re.sub(r'[^a-zA-Z0-9@. ]', '', input_string)
        data = {key: sanitize(str(value)) for key, value in data.items()}

        # print to console for debugging
        print(json.dumps(data, indent=4))

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_data = f"{timestamp}: {json.dumps(data)}\n"

        with open("submissions.txt", "a") as file:
            file.write(formatted_data)
        return 'Submission successful!'
    except Exception as e:
        logging.error(f"Error processing the request: {e}", exc_info=True)
        return "Failed to record submission", 500
    
if __name__ == '__main__':
    app.run(debug=True)