from flask import Flask, request, jsonify
from flask.views import MethodView
import json
from settings import APP_ROOT, USER_NAME
import os

def read_user_info():
    with open(os.path.join(APP_ROOT, 'users.json')) as f:
        data = json.loads(f.read())
    
    if data is None:
        return jsonify('Error: Missing user list.')

    users = data['users']
    return users

def write_user_info(users):
    info = str(users).replace("'", '"')
        
    with open(os.path.join(APP_ROOT, 'users.json'), 'w') as f:
        data = "{\"users\": " + str(info) + "}"
        f.write(data)

def get_data():
    if not request.json or not 'name' in request.json:
        return 'Error: No information provided. Please porivde the user information.'
    data = request.json
    return data


app = Flask(__name__)

class API_USERS(MethodView):
    def get(self):
        if 'name' in request.args:
            #name = str(request.args.get('name'))
            name = request.args['name']
        else:
            return 'Error: No name provided. Please specify a user.'

        users = read_user_info()
        #return str(users)

        for user in users:
            if user['name'] == str(name):
                return json.dumps(user)
        return jsonify(name + ': this user dosen\'t exist!') 
                
    def post(self):
        data = get_data()
        
        if data is None:
            return 'User information is incorrect!'
        else:
            rname = data['name']
            #return jsonify(data['communicate_information'])
        #return rname
                 
        for name in USER_NAME:
            if rname == name:
                return 'The user has been created! '
        USER_NAME.append(rname)   
        
        users = read_user_info()

        info = {
            'name': data['name'],
            'job_title': data['job_title'],
            'communicate_information': {
                "email": data['communicate_information']['email'], 
                "mobile": data['communicate_information']['mobile']
            }
        }
        users.append(info)
        write_user_info(users)

        #return str(users)
        
        return jsonify(message = rname + ' has been created!\n')
    def put(self):
        data = get_data()
        
        rname = data['name']
        
        users = read_user_info()

        for user in users:
            if user['name'] == rname:
                user.update(data)           
                write_user_info(users)
                return rname + ' has been updated! ' + '\n' + str(user)
        return rname + ': the user is not in the system.' 

    def delete(self):
        data = get_data()
        count = 0
        users = read_user_info()
        for user in users:
            if user['name'] == data['name']:
                users.pop(count)
                write_user_info(users)
                return data['name'] + ' has been deleted!'
            count += 1
        return data['name'] + ': the user is not in the system.' 

app.add_url_rule('/users/', view_func=API_USERS.as_view('users'))

@app.route('/users/list', methods=['GET']) 
def login2():
    users = read_user_info()

    return jsonify({'users': users})

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")    