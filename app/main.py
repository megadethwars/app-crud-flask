# /run.py
import os
#from dotenv import load_dotenv, find_dotenv
import logging
logging.getLogger().setLevel(logging.INFO)
from src.appinit import create_app


#load_dotenv(find_dotenv())
env_name = os.getenv('FLASK_ENV')

logging.info("envirorment - "+str(env_name))
app = create_app(env_name)

if __name__ == '__main__':
  port = os.getenv('FLASK_PORT')
  # run app
  app.run(host='0.0.0.0', port=port)