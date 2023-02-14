import requests
import random
import string
import time

# Define base URL for API calls
base_url = 'http://localhost:8081'

# Define test users
admin_user = {'username': 'adminuser', 'password': 'adminpassword'}
basic_user = {'username': 'user', 'password': 'password'}

# Login API test
def test_login():
    res = requests.post(f'{base_url}/login', data=admin_user)
    print(res.text, res.status_code, '\n')
    assert res.status_code == 200
    
# Create user API test
def test_create_user(username):
    # Test with a non-admin user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload = {
        'user': basic_user['username'], 
        'username': username, 
        'password': ''.join(random.choices(string.ascii_letters + string.digits, k=8)), 
        'role': 'basic'
    }
    res = requests.post(f'{base_url}/admin/create_user', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 403

    # Test with an admin user
    login_response = requests.post(f'{base_url}/login', data=admin_user)
    payload['user'] = admin_user['username']
    res = requests.post(f'{base_url}/admin/create_user', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 201

# Edit user API test
def test_edit_user(username):
    # Test with a non-admin user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload = {
        'user': basic_user['username'], 
        'username': username, 
        'role': 'admin'
    }
    res = requests.put(f'{base_url}/admin/edit_user', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 403

    # Test with an admin user
    login_response = requests.post(f'{base_url}/login', data=admin_user)
    payload['user'] = admin_user['username']
    res = requests.put(f'{base_url}/admin/edit_user', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.status_code, '\n')
    assert res.status_code == 204

# Create Group API test
def test_create_group(groupname):
    # Test with a any user {'admin','non-admin'}
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload = {
        'user': basic_user['username'], 
        'name': groupname
    }
    res = requests.post(f'{base_url}/group/create', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 201

# Add Member API test
def test_add_member(groupname, member):
    # Test with a non group-admin user
    # NOTE: Group-admin is different from admin-user
    login_response = requests.post(f'{base_url}/login', data=admin_user)
    payload = {
        'user': admin_user['username'], 
        'name': groupname,
        'member': member
    }
    res = requests.put(f'{base_url}/group/add_member', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 422

    # Test with a group-admin user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['user'] = basic_user['username']
    res = requests.put(f'{base_url}/group/add_member', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.status_code, '\n')
    assert res.status_code == 204

    # Test with a non-existant user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['member'] = 'nonuser'
    res = requests.put(f'{base_url}/group/add_member', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 404

    # Test with a non-existant group
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['name'] = 'nongroup'
    res = requests.put(f'{base_url}/group/add_member', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 404

# View Members API test
def test_view_members(groupname):
    # Test with a non-member user
    # NOTE: Group-admin is different from admin-user
    login_response = requests.post(f'{base_url}/login', data=admin_user)
    payload = {
        'user': admin_user['username'], 
        'name': groupname,
    }
    res = requests.get(f'{base_url}/group/view_members', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 422

    # Test with a member user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['user'] = basic_user['username']
    res = requests.get(f'{base_url}/group/view_members', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 200

    # Test with a non-existant group
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['name'] = 'nongroup'
    res = requests.get(f'{base_url}/group/view_members', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 404

# Delete Group API test
def test_delete_group(groupname):
    # Test with non group-admin user
    login_response = requests.post(f'{base_url}/login', data=admin_user)
    payload = {
        'user': admin_user['username'], 
        'name': groupname
    }
    res = requests.delete(f'{base_url}/group/delete', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 403

    # Test with a group-admin user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['user'] = basic_user['username']
    res = requests.delete(f'{base_url}/group/delete', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.status_code, '\n')
    assert res.status_code == 204

    # Test with non group-existant group
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    res = requests.delete(f'{base_url}/group/delete', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 404

# Send Message API test
def test_send_message(groupname):
    # Test with a non-member user
    login_response = requests.post(f'{base_url}/login', data=admin_user)
    payload = {
        'user': admin_user['username'], 
        'group_name': groupname,
        'message': 'Hello World'
    }
    res = requests.post(f'{base_url}/group/send_message', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 422

    # Test with a member user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['user'] = basic_user['username']
    res = requests.post(f'{base_url}/group/send_message', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    time.sleep(1)
    payload['message'] = 'second message'
    requests.post(f'{base_url}/group/send_message', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 201

    # Test with non group-existant group
    payload['group_name'] = 'nongroup'
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    res = requests.post(f'{base_url}/group/send_message', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 404

# View Messages API test
def test_get_messages(groupname):
    # Test with a non-member user
    login_response = requests.post(f'{base_url}/login', data=admin_user)
    payload = {
        'user': admin_user['username'], 
        'group_name': groupname
    }
    res = requests.get(f'{base_url}/group/get_messages', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 422

    # Test with a member user
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    payload['user'] = basic_user['username']
    res = requests.get(f'{base_url}/group/get_messages', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 200

    # Test with non group-existant group
    payload['group_name'] = 'nongroup'
    login_response = requests.post(f'{base_url}/login', data=basic_user)
    res = requests.get(f'{base_url}/group/get_messages', data=payload, headers={'Cookie': f'session={login_response.cookies["session"]}'})
    print(res.text, res.status_code, '\n')
    assert res.status_code == 404


# Logout API test
def test_logout():
    res = requests.post(f'{base_url}/login', data=admin_user)
    res = requests.post(f'{base_url}/logout')
    print(res.text, res.status_code, '\n')
    assert res.status_code == 200


if __name__ == '__main__':
    # Run tests
    """Please change the variables declared below everytime you run the script. 
    Running the script creates entries in DB which may give assertion errors 
    when you run the script agian with the same arguments."""

    #change these variables
    username = "phantom"
    groupname = "phantomzone"
    member = username

    tests = [
        test_login,
        test_create_user,
        test_edit_user,
        test_create_group,
        test_add_member,
        test_view_members,
        test_delete_group,
        test_create_group,
        test_send_message,
        test_get_messages,
        test_logout
    ]

    count = 0 
    passed = 0 

    for test in tests:
        try:
            if test in {test_login, test_logout}:
                test()
            elif test == test_add_member:
                test(groupname, member)
            else:
                test(groupname)
            count += 1
        except:
            print(f'Test case failed for {test.__name__}', '\n')
            continue
        finally:
            passed += 1

    print('\n')
    print(f"------------------{count}/{passed} test cases passed------------------")
