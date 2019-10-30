from flask import Flask, request
import json


def validate_username(name):
    char = any((((char >= 'a') and (char <= 'z')) or ((char >= 'A') and (char <= 'Z'))) for char in name)
    # Checks if there is at least one letter
    if char is False:
        return 'There must be a letter'
    return True


def validate_password(password):
    if len(password) < 8:
        # Checks if the password is more than 8 digits
        return 'String must be at least 8 characters long'

    low = any(((char >= 'a') and (char <= 'z')) for char in password)
    # Checks if there is at least one lowercase letter
    up = any(((char >= 'A') and (char <= 'Z')) for char in password)
    # Checks if there is at least one uppercase letter
    if low is False and up is False:
        return 'There must be a lowercase and uppercase letter'
    elif low is False:
        return 'There must be a lowercase letter'
    elif up is False:
        return 'There must be a uppercase letter'
    return True


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Just a regular key for now'

data = [dict()]  # list of dictionary


@app.route("/")
@app.route('/Registration', methods=['GET', 'POST'])  # allow both GET and POST requests
def registration():
    if request.method == 'POST':
        user_id = 0  # Initializes a list of dictionary entries for each subscriber
        username = request.form.get('username')
        password = request.form.get('password')
        if validate_password(password) is not True:
            # Checking password valid
            return f'{validate_password(password)}, Please try again'
        elif validate_username(username) is not True:
            # Checking username valid
            return f'{validate_username(username)}, Please try again'
        data[user_id][username] = password
        data_to_json = json.dumps(data[user_id])  # convert into JSON
        user_id += 1  # Increases id

        return 'registration succeeded!'

    return '''<form method="POST" action="/Registration">
                      Username: <input type="text" name="username"><br>
                      Password: <input type="password" name="password"><br>
                      <input type="submit" value="registration"><br>
                  </form>'''


@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''<form method="POST" action="/Login">
                              Username: <input type="text" name="username"><br>
                              Password: <input type="password" name="password"><br>
                              <input type="submit" value="Login"><br>
                          </form>'''

    for dictionary in data:
        if(request.form.get('password') in dictionary.values()) and (request.form.get('username') in dictionary.keys()):
            # Checks username and password
            return 'TOKEN'
        else:
            return 'you are not registered'


@app.route('/Token', methods=['GET', 'POST'])
def token():
    if request.method == 'GET':
        return '''<form method="POST" action="/Token">
                              Token: <input type="text" name="token"><br>
                              Text: <input type="text" name="text"><br>
                              <input type="submit" value="check"><br>
                          </form>'''
    if request.form.get('token') == request.args.get('token'):
        # Checks token
        print(request.form.get('text'))
    else:
        print('token is invalid')
    return 'The token was checked'


#  Take care of updating the server
if __name__ == '__main__':
    app.run(debug=True)

