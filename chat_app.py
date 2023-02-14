from flask import Flask, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from connections import users_collection, groups_collection, messages_collection
from datetime import datetime
import traceback

app = Flask(__name__)

app.secret_key = "7A244226452948404D63516A5EWD3T6E5A7234753778214125442A462D4"

users    = users_collection()
groups   = groups_collection()
messages = messages_collection()

# Helper function to check if the user is an admin
def is_admin(username):
    user = users.find_one({'username': username})
    if user and user['role'] == 'admin':
        return True
    return False

def is_superuser(username):
    user = users.find_one({'username': username})
    if user and user['role'] == 'superuser':
        return True
    return False

@app.route('/')
def index():
    return 'Welcome to chat_app!'


# Authentication APIs
@app.route('/login', methods=['POST'])
def login():
    try:
        try:
            username = request.form['username']
            password = request.form['password']
        except:
            traceback.print_exc()
            return 'Login Failed.', 400
        user = users.find_one({'username': username})
        if not user:
            return 'Incorrect username', 401
        if not check_password_hash(user['password_hash'], password):
            return 'Incorrect password.', 401
        session["username"] = username
        return 'Login successful.', 200
    except:
        traceback.print_exc()
        return 'Login Failed.', 500
    
@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return 'Logout successful.', 200
    except:
        traceback.print_exc()
        return 'Logout Failed.', 500


# Admin APIs
@app.route('/admin/create_user', methods=['POST'])
def create_user():
    try:
        try:
            user = request.form['user']
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
        except:
            traceback.print_exc()
            return 'Could not create user.', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        if not (is_admin(user) or is_superuser(user)):
            return 'Only admin can create users.', 403
        role = role if role != '' else 'basic'
        if role not in {'admin', 'basic'}:
            return 'Invalid role specified', 422
        if users.find_one({'username': username}):
            return 'User already exists', 422
        new_user = {
            'username': username,
            'role': role,
            'password_hash': generate_password_hash(password),
        }
        users.insert_one(new_user)
        return 'User created successfully.', 201
    except:
        traceback.print_exc()
        return 'Could not create User.', 500

@app.route('/admin/edit_user', methods=['PUT'])
def edit_user():
    try:
        try:
            user = request.form['user']
            username = request.form['username']
            role = request.form['role']
        except:
            traceback.print_exc()
            return 'Could not edit user.', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        if not (is_admin(user) or is_superuser(user)):
            return 'Only admin can edit users.', 403
        usr = users.find_one({'username': username})
        if not usr:
            return 'User not found.', 404
        if usr['role'] == 'admin' and not is_superuser(user):
            return 'Cannot edit admin.', 403
        role = role if role != '' else 'basic'
        if role not in {'admin', 'basic'}:
            return 'Invalid role specified', 422
        users.update_one({'username': username}, {"$set":{"role":role}})
        return '', 204
    except:
        traceback.print_exc()
        return 'Could not edit user.', 500
    

# Group APIs
@app.route('/group/create', methods=['POST'])
def create_group():
    try:
        try:
            user = request.form['user']
            group_name = request.form['name']
        except:
            traceback.print_exc()
            return 'Could not create group.', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        if groups.find_one({'name': group_name}):
            return 'Group already exists', 422
        group = {
            'name': group_name,
            'members': [user],
            'group_admins': [user]
        }
        groups.insert_one(group)
        return 'Group created successfully.', 201
    except:
        traceback.print_exc()
        return 'Could not create group.', 500

@app.route('/group/search')
def search_group():
    try:
        try:
            user = request.form['user']
        except:
            traceback.print_exc()
            return 'Could not retrieve groups.', 400   
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        if not is_superuser(user):
            return 'Insufficient privilages to access ths API', 403
        group_names = [group['name'] for group in groups.find({})]
        return '\n'.join(group_names), 200
    except:
        traceback.print_exc()
        return 'Could not retrieve groups.', 500

@app.route('/group/add_member', methods=['PUT'])
def add_member():
    try:
        try:
            user = request.form['user']
            group_name = request.form['name']
            member = request.form['member']
        except:
            traceback.print_exc()
            return 'Could not add user to group.', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        group = groups.find_one({'name': group_name})
        if group:
            if not (user in group["group_admins"] or is_superuser(user)):
                return 'Only group admins can add members.', 422
            if not users.find_one({'username': member}):
                return 'User does not exist', 404
            if member not in group["members"]:
                group['members'].append(member)
                groups.update_one({'name': group_name}, {"$set":{"members": group['members']}})
                return '', 204
            return 'Member already exists in group', 422
        return 'Group not found.', 404
    except:
        traceback.print_exc()
        return 'Could not add user to group.', 500

@app.route('/group/view_members')
def view_members():
    try:
        try:
            user = request.form['user']
            name = request.form['name']
        except:
            traceback.print_exc()
            return 'Could not view members.', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        group = groups.find_one({'name': name})
        if group:
            if not (user in group["members"] or is_superuser(user)):
                return 'User not in group.', 422
            return group['members'], 200
        return 'Group not found.', 404
    except:
        traceback.print_exc()
        return 'Could not view members.', 500

@app.route('/group/delete', methods=['DELETE'])
def delete_group():
    try:
        try:
            user = request.form['user']
            group_name = request.form['name']
        except:
            traceback.print_exc()
            return 'Could not delete group.', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        group = groups.find_one({'name': group_name})
        if group:
            if not (user in group['group_admins'] or is_superuser(user)):
                return 'Only Group Admins can delete group.', 403
            groups.delete_one({'name': group_name})
            return '', 204
        return 'Group not found.', 404
    except:
        traceback.print_exc()
        return 'Could not delete group.', 500


# Group Messages
@app.route('/group/send_message', methods=['POST'])
def send_message():
    try:
        try:
            user = request.form['user']
            msg = request.form['message']
            group_name = request.form['group_name']
        except:
            traceback.print_exc()
            return 'Could not send message.', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        group = groups.find_one({'name': group_name})
        if group:
            if user not in group["members"]:
                return 'User not in group.', 422
            message = {
                'group': group_name,
                'user': user,
                'message': msg,
                'timestamp': datetime.now()
            }
            messages.insert_one(message)
            return 'Message sent.', 201
        return 'Group not found.', 404
    except:
        traceback.print_exc()
        return 'Could not send message.', 500

@app.route('/group/get_messages')
def get_messages():
    try:
        try:
            user = request.form['user']
            group_name = request.form['group_name']
        except:
            traceback.print_exc()
            return 'Could not retrieve messages', 400
        if not ('username' in session and session["username"] == user):
            return 'Login to access this API', 401
        group = groups.find_one({'name': group_name})
        if group:
            if user not in group["members"]:
                return 'User not in group.', 422
            msgs = messages.find(({'group': group_name}))
            messages_list = [(m['user'], m['message'], m['timestamp']) for m in msgs]
            return sorted(messages_list, key=lambda x: x[2]), 200
        return 'Group not found.', 404
    except:
        traceback.print_exc()
        return 'Could not retrieve messages', 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=False)