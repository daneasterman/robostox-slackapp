import os
from dotenv import load_dotenv

load_dotenv()

DEPLOY_ENV = os.getenv('DEPLOY_ENV')

if DEPLOY_ENV == "development":
	SLACK_SIGNING_SECRET = os.getenv('DEV_SLACK_SIGNING_SECRET')
else:
	SLACK_SIGNING_SECRET = os.getenv('PROD_SLACK_SIGNING_SECRET')

if DEPLOY_ENV == "development":
	SLACK_CLIENT_ID = os.getenv('DEV_SLACK_CLIENT_ID')
else:
	SLACK_CLIENT_ID = os.getenv('PROD_SLACK_CLIENT_ID')

if DEPLOY_ENV == "development":
	SLACK_CLIENT_SECRET = os.getenv('DEV_SLACK_CLIENT_SECRET')
else:
	SLACK_CLIENT_SECRET = os.getenv('PROD_SLACK_CLIENT_SECRET')