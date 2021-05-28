import os
import socketio
from dotenv import load_dotenv

load_dotenv()

SEC_API_KEY = str(os.getenv('SEC_API_KEY'))
SEC_ENDPOINT = f'https://api.sec-api.io:3334?apiKey={SEC_API_KEY}'
sio = socketio.Client()
 
@sio.on('connect', namespace='/all-filings')
def on_connect():
    print("Connected to https://api.sec-api.io:3334/all-filings")
 
@sio.on('filing', namespace='/all-filings')
def on_filings(filing):
    print(filing)
 
sio.connect(SEC_ENDPOINT, namespaces=['/all-filings'])
sio.wait()