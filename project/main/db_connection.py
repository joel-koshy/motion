from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import environ

env = environ.FileAwareEnv()
environ.Env.read_env()

uri = env('DB_URL')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

