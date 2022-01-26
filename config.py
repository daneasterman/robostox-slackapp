import os
from dotenv import load_dotenv

load_dotenv()
DEPLOY_ENV = os.getenv('DEPLOY_ENV')

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# DEV VARS ARE IN .ENV (UNTRACKED DUE TO .GITIGNORE)
# PROD VARS ARE IN PRIVATE HEROKU SETTINGS (CONFIG VARS)

if DEPLOY_ENV == "development":
	SLACK_SIGNING_SECRET = os.getenv('DEV_SLACK_SIGNING_SECRET')
elif DEPLOY_ENV == "production":
	SLACK_SIGNING_SECRET = os.getenv('PROD_SLACK_SIGNING_SECRET')

if DEPLOY_ENV == "development":
	SLACK_CLIENT_ID = os.getenv('DEV_SLACK_CLIENT_ID')
elif DEPLOY_ENV == "production":
	SLACK_CLIENT_ID = os.getenv('PROD_SLACK_CLIENT_ID')

if DEPLOY_ENV == "development":
	SLACK_CLIENT_SECRET = os.getenv('DEV_SLACK_CLIENT_SECRET')
elif DEPLOY_ENV == "production":
	SLACK_CLIENT_SECRET = os.getenv('PROD_SLACK_CLIENT_SECRET')