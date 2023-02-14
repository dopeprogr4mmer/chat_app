from pymongo import MongoClient 
from datetime import datetime

CLUSTER = MongoClient("mongodb+srv://ph4ntomphoenix:qjwPqGnA2CVCykPw@phantomzone.a2drk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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