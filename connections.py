from pymongo import MongoClient 
from datetime import datetime
from config import mongo_url

CLUSTER = MongoClient(mongo_url)
DB = 'chat_app'

def users_collection():
	collection = CLUSTER[DB]['users']
	return collection

def groups_collection():
	collection = CLUSTER[DB]['groups']
	return collection

def messages_collection():
	collection = CLUSTER[DB]['messages']
	return collection
