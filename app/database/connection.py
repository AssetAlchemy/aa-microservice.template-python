from pymongo import MongoClient
import gridfs

from config.envs import db_uri, db_name


# Connecting to database
client = MongoClient(db_uri)
db = client[db_name]

# Creating gridFS object
fs = gridfs.GridFS(db, "uploads")
