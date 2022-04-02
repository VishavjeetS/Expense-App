import mysql.connector
from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
# MySql Connect
connection = mysql.connector.connect(host='localhost',
                                     database='Expense',
                                     user='root',
                                     password='Root@1234')

cursor = connection.cursor()


@app.route("/")
def login():
    if 'id' in session:
        return redirect('/home')
    else:
        return render_template('login.html')


@app.route("/register")
def register():
    return render_template('register.html')


@app.route('/home')
def home():
    if 'id' in session:
        return render_template('home.html')
    else:
        return redirect("/")


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_val():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("""SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'""".format(email, password))
    users = cursor.fetchall()
    print(users)
    if len(users) > 0:
        session['id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')


@app.route("/register_user", methods=['POST'])
def register_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute(
        """INSERT INTO USERS (id, name, email, password) VALUES (NULL,'{}', '{}', '{}')""".format(name,
                                                                                                  email, password))
    connection.commit()
    users = cursor.fetchall()
    print(users)
    return redirect('/home')


if __name__ == "__main__":
    app.run(debug=True)
