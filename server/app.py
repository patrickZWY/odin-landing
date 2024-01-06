"""
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
def send_to_database():
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
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import re
import signal
import sys

def validate_name(f):
    def wrapper(*args, **kwargs):
        name = request.json.get('name', '')
        if not re.match(r'^[a-zA-Z\s]{2,50}$', name):
            return "Invalid name", 400
        # sending the same send_to_database function to next decorator
        return f(*args, **kwargs)
    return wrapper

def validate_email(f):
    def wrapper(*args, **kwargs):
        email = request.json.get('email', '')
        if not re.match(r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$', email):
            return "Invalid email", 400
        return f(*args, **kwargs)
    return wrapper

def validate_message(f):
    def wrapper(*args, **kwargs):
        message = request.json.get('message', '')
        if not(len(message) > 0 and len(message) < 500):
            return "Invalid message", 400
        return f(*args, **kwargs)
    return wrapper

def sanitize(input_string):
    return re.sub(r'[^a-zA-Z0-9@!?()&. ]', '', input_string)


def graceful_shutdown(sig, frame):
    logging.info('Shut down gracefully')
    sys.exit(0)
# Ctrl-C
signal.signal(signal.SIGINT, graceful_shutdown)
# kill command
signal.signal(signal.SIGTERM, graceful_shutdown)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Submission {self.name}>"

limiter = Limiter(
    app,
    default_limits=["200 per day", "20 per hour"]
)

logging.basicConfig(level=logging.ERROR,
                    filename='errorlog.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
# verifying if server is working

@app.route('/')
def home():
    return 'Welcome to the Contact Form Server!'

@app.route('/submissions')
def get_submissions():
    submissions = Submission.query.all()
    return jsonify([{'name': s.name, 'email' : s.email, 'message': s.message, 'timestamp':s.timestamp.isoformat()} for s in submissions])

# handling submission
@app.route('/send', methods=['POST'])
@limiter.limit("4/minute")
@validate_name
@validate_email
@validate_message
def send_to_database():
    try:
        data = request.json
        data = {key: sanitize(str(value)) for key, value in data.items()}

        new_submission = Submission(
            name=data['name'],
            email=data['email'],
            message=data['message']
        )

        db.session.add(new_submission)
        db.session.commit()

        return 'Submission successful!'
    except Exception as e:
        logging.error(f"Error processing the request: {e}", exc_info=True)
        return "Failed to record submission", 500
"""
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
"""

if __name__ == '__main__':
    app.run(debug=True)
